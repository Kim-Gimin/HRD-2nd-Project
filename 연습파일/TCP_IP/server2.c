#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <errno.h>

#define MAX_CLIENT 100
#define MAX_MESSAGE 1024

// Define a message buffer structure
struct msgbuf {
    long mtype;
    char mtext[MAX_MESSAGE];
};

// Define a client structure
typedef struct client {
    int id;
    char name[20];
    int sock;
    int msqid;
} Client;

void error_handling(const char* message) {
    perror(message);
    exit(1);
}

void send_message(Client* client, char* message) {
    int i;
    struct msgbuf buf;

    // Copy the message to the buffer
    strcpy(buf.mtext, message);

    // Set the message type
    buf.mtype = client->id;

    // Send the message to all clients
    for (i = 0; i < MAX_CLIENT; i++) {
        if (clients[i].id != 0 && client->id != clients[i].id) {
            if (msgsnd(clients[i].msqid, (void*)&buf, MAX_MESSAGE, IPC_NOWAIT) == -1) {
                error_handling("msgsnd() error");
            }
        }
    }
}

void* handling_client(void* arg) {
    Client client = *(Client*)arg;
    char message[MAX_MESSAGE];
    int str_len;

    while ((str_len = read(client.sock, message, MAX_MESSAGE)) != 0) {
        message[str_len] = 0;
        printf("[Client %d] %s\n", client.id, message);
        send_message(&client, message);
    }

    close(client.sock);
    client.id = 0;
    client.name[0] = 0;

    return NULL;
}

void* handling_message(void* arg)
{
    struct msgbuf msg;
    int rcv_size;
    while (1) {
    // Receive message from the message queue
    rcv_size = msgrcv(msqid, &msg, MAX_MESSAGE, 0, 0);
    if (rcv_size == -1) {
        error_handling("msgrcv() error");
    }

    // Send the message to all clients
    for (int i = 0; i < MAX_CLIENT; i++) {
        if (clients[i].sock != 0) {
            send_message(&clients[i], msg.mtext);
        }
    }

    // If the message is "exit", then stop the message handling thread
    if (strcmp(msg.mtext, "exit") == 0) {
        pthread_exit(NULL);
    }
}

return NULL;
}

void send_message(Client* client, char* message)
{
// Send the message to the client using the message queue
    struct msgbuf msg;
    msg.mtype = client->id;
    strncpy(msg.mtext, message, MAX_MESSAGE);
    if (msgsnd(client->msqid, &msg, strlen(msg.mtext) + 1, 0) == -1) {
    error_handling("msgsnd() error");
    }
}
