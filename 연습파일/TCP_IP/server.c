#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#define MAX_CLIENT_NUM 5
#define NAME_SIZE 20

void* handling_client(void* arg);
void* send_message(void*);
void error_handling(const char*);
char message[BUFSIZ] = {'\0', };

int client_num = 0;
int client_socks[MAX_CLIENT_NUM];
pthread_mutex_t mutex;
char name[NAME_SIZE] = {'\0', };
char name_message[BUFSIZ] = {'\0', };

void* send_message(void * args)
{
    int sock = *((int*)args);
    char name_message[NAME_SIZE + BUFSIZ] = {'\0',};
    int str_length = 0;
    while(true)
    {
        fgets(message, BUFSIZ, stdin);
        if(!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
        {
        close(sock);
        exit(0);
        }
        sprintf(name_message, "%s : %s", name, message);
        write(sock, name_message, strlen(name_message));



    }

    return NULL;
}

int main(int argc, char* argv[])
{
    int serv_sock = 0, client_sock = 0;
    struct sockaddr_in serv_addr, client_addr;
    socklen_t client_addr_size = 0;
    pthread_t thread = 0ul;
    void* thread_return = NULL;

    if(argc != 2)
    {
        error_handling("Usage : ./chat_server <port>");
    }

    if(pthread_mutex_init(&mutex, NULL) != 0)
    {
        error_handling("mutex initialization error");
    }

    serv_sock = socket(PF_INET, SOCK_STREAM, 0);
    if(serv_sock == -1)
    {
        error_handling("socket() error");
    }

    memset(&serv_addr, 0, sizeof serv_addr);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));

    if(bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof serv_addr) == -1)
    {
        error_handling("bind() error");
    }

    if(listen(serv_sock, MAX_CLIENT_NUM) == -1)
    {
        error_handling("listen() error");
    }
    close(serv_sock);
    pthread_mutex_destroy(&mutex);

    return 0;
}
void error_handling(const char* _message)
{
    fputs(_message, stdout);
    fputs("\r\n", stdout);
    exit(1);
}
void* handling_client(void* arg)
{
    int client_sock = *((int*)arg);
    int str_len = 0;
    char message[BUFSIZ] = {'\0', };
    char name_message[BUFSIZ] = {'\0', };

    pthread_mutex_lock(&mutex);
    client_num--;
    pthread_mutex_unlock(&mutex);


    pthread_mutex_lock(&mutex);
    for(int i = 0; i < client_num; ++i)
    {
        if(client_sock == client_socks[i])
        {
            while(i++ < client_num - 1)
            {
                client_socks[i - 1] = client_socks[i];
            }
            break;
        }
    }
    client_num--;
    pthread_mutex_unlock(&mutex);
    close(client_sock);

    return NULL;
}