#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <netinet/in.h>
#include <time.h>

#define MAX_CLIENT 256
int client_count = 0;
int client_sockets[MAX_CLIENT] = {0,};
pthread_mutex_t mutex_key = PTHREAD_MUTEX_INITIALIZER;  //  mutex_key 초기화

int answer[3] = {0,};

void error_handling(const char*);
void sending_message(const char*, int);
void* handling_client(void*);   //  task function

bool check_guess(int guess[]);
char* create_result_message(int guess[]);

int main(int argc, const char * argv[])
{
    srand(time(NULL));  //  rand() 함수를 사용하기 전에 srand() 함수로 시드값을 초기화합니다.
    answer[0] = rand() % 9 + 1;  //  1부터 9까지의 무작위 수를 생성하여 answer 배열에 저장합니다.
    for (int i = 1; i < 3; i++)
    {
        int temp = rand() % 9 + 1;
        //  이전에 생성된 수와 중복되지 않도록 새로운 수를 생성합니다.
        while (temp == answer[i - 1])
        {
            temp = rand() % 9 + 1;
        }
        answer[i] = temp;
    }
    int serv_sock = 0;
    int clnt_sock = 0;
    struct sockaddr_in serv_addr;
    struct sockaddr_in clnt_addr;
    memset(&serv_addr, 0, sizeof serv_addr);
    memset(&clnt_addr, 0, sizeof clnt_addr);

    int client_addr_size = 0;
    pthread_t pthread_id = 0ul;
    if(argc != 2)
    {
        error_handling("MULTI_THREAD_CHAT_SERVER 9999");
    }
    pthread_mutex_init(&mutex_key, NULL);
    if((serv_sock = socket(PF_INET, SOCK_STREAM, 0)) == -1)
    {
        error_handling("socket() error");
    }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    if(bind(serv_sock, (const struct sockaddr*)&serv_addr, sizeof serv_addr) == -1)
    {
            
        error_handling("bind() error");
    }
    if(listen(serv_sock, 5) == -1)
    {
        error_handling("listen() error");
    }
    while(true)
    {
        client_addr_size = sizeof clnt_addr;
        if((clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, (socklen_t*)&client_addr_size)) == -1)
        {               
            error_handling("accept() error");
        }
        pthread_mutex_lock(&mutex_key);
        client_sockets[client_count++] = clnt_sock;
        pthread_mutex_unlock(&mutex_key);
        pthread_create(&pthread_id, NULL, handling_client, (void*)&clnt_sock);
        pthread_detach(pthread_id);
        fprintf(stdout, "Connected Client IP : %s\r\n", inet_ntoa(clnt_addr.sin_addr));
}
    close(serv_sock);
    return 0;
}
void error_handling(const char* _message)
{
    fputs(_message, stderr);
    fputs("\r\n", stderr);
    exit(1);
    return;
}
void sending_message(const char* _message, int _str_length)
{
    pthread_mutex_lock(&mutex_key);
    for(int i = 0; i < client_count; ++i)
    {
        write(client_sockets[i], _message, _str_length);
    }
    pthread_mutex_unlock(&mutex_key);
    return;
}
void* handling_client(void * args)
{
    int client_sock = *((int*)args);
    int str_length = 0;
    char message[BUFSIZ] = {'\0', };
    int guess[3] = {0};
    
    while((str_length = read(client_sock, message, BUFSIZ - 1)) != 0) 
    {
        sscanf(message, "%d %d %d\n", &guess[0], &guess[1], &guess[2]);
        if (check_guess(guess))
        {
            sending_message("Congratulations, you guessed the correct numbers!", strlen("Congratulations, you guessed the correct numbers!"));
            break;
        }
        else
        {
            char* result_message = create_result_message(guess);
            sending_message(result_message, strlen(result_message));
            free(result_message);
        }
    }
    
    --client_count;
    pthread_mutex_unlock(&mutex_key);
    close(client_sock);
    
    return NULL;
}
bool check_guess(int guess[])
{
    for (int i = 0; i < 3; i++)
    {
        if (guess[i] != answer[i])
        {
            return false;
        }
    }
    return true;
}

char* create_result_message(int guess[])
{
    int strikes = 0;
    int balls = 0;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (guess[i] == answer[j])
            {
                if (i == j)
                {
                    strikes++;
                }
                else
                {
                    balls++;
                }
            }
        }
    }
    char* result_message = (char*)malloc(50);
    snprintf(result_message, 50, "Strikes: %d, Balls: %d\n\n", strikes, balls);
    return result_message;
}
