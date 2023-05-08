#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>

#define NAME_SIZE 20

void* sending_message(void*);
void* receive_message(void*);
void error_handling(const char *);
char message[BUFSIZ] = {'\0', };

int main(int argc, const char* argv[])
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    pthread_t send_thread = 0ul;
    pthread_t receive_thread = 0ul;
    void* thread_return = NULL; //thread 종료될때 NULL로 받겠다.

    if(argc != 3)
    {
        error_handling("Usage : ./client ip port ");
    }

    if((sock = socket(PF_INET, SOCK_STREAM, 0)) == -1)
    {
        error_handling("socket() error");
    }

    memset(&serv_addr, 0, sizeof serv_addr);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
    serv_addr.sin_port = htons(atoi(argv[2]));

    if(connect(sock, (const struct sockaddr*)&serv_addr, sizeof serv_addr) == -1)
    {
        error_handling("connect() error");
    }

    char name[NAME_SIZE] = {'\0', };
    sprintf(name,"[%s]", argv[3]);

    write(sock, name, strlen(name)); //클라이언트가 서버에 자신의 닉네임을 전송

    pthread_create(&send_thread, NULL,sending_message,(void*)&sock);
    pthread_create(&receive_thread, NULL, receive_message, (void*)&sock);
    pthread_join(send_thread, &thread_return);
    pthread_join(receive_thread, NULL);

    close(sock);

    return 0;
}

// task function
void* sending_message(void* args)
{
    int sock = *((int*)args);
    char message[BUFSIZ] = {'\0', };
    int str_length = 0;

    while(true)
    {
        fgets(message, BUFSIZ, stdin);

        if(!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
        {
            close(sock);
            exit(0);
        }

        write(sock, message, strlen(message));
    }

    return NULL;
}

void* receive_message(void* args)
{
    int sock = *((int*)args);
    char message[BUFSIZ] = {'\0', };
    int str_length = 0;

    while(true)
    {
        if((str_length = read(sock, message, BUFSIZ - 1)) == -1)
        {
            return NULL;
        }

        message[str_length]= '\0';
        fputs(message, stdout);
    }

    return NULL;
}

void error_handling(const char* _message)
{
    fputs(_message, stderr);
    fputs("\n",stderr);
    exit(1);
    return;
}
