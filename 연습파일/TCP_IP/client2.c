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
//char name[NAME_SIZE] = {'\0', };
char message[BUFSIZ] = {'\0', };

int main(int argc, const char* argv[])
{
    int sock = 0;
    struct sockaddr_in serv_addr;
    pthread_t send_thread = 0ul;
    pthread_t receive_thread = 0ul;
    void* thread_return = NULL;
    if(argc != 3)
    {
        error_handling("MULTI_THREAD_CHAT_ClIENT SERVER_IP 9999");
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

    pthread_create(&send_thread, NULL,sending_message,(void*)&sock);
    pthread_create(&receive_thread, NULL, receive_message, (void*)&sock);
    pthread_join(send_thread, &thread_return);
    pthread_join(receive_thread, NULL);
    close(sock);

    return 0;
}

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
        str_length = read(sock, message, BUFSIZ - 1);
        message[str_length] = '\0';
        fputs(message, stdout);
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
        printf("%s", message);
    }
    return NULL;
}

void error_handling(const char* _message)
{
    fputs(_message, stderr);
    fputs("\r\n",stderr);
    exit(1);
    return;
}