11/21/25
[[HomeLab]]
I downloaded QEMU/KVM and virt-manager for this project, i then installed a copy of a windows 10 ltsc enterprise from massgrave. I dont need a product key because i can reset it when 90 days run out with this command.

`slmgr /rearm` Just open cmd as admin inside the win10 vm then input this command and reboot, it will reset the timer back to 90 days. but this can only be done 3 times.

I then installed an ubuntu server where i will run wazuh, and possibly a waf. Im currently in the stage where im downloading the wazuh, and generating security certificates. To be fully transparent, i came across a problem where my ubuntu server was not connecting to my internet via nat, i had to create a config in /etc/netplan/ named 01-netcfg.yaml.

`/etc/netplan/01-netcfg.yaml`
`network:`
  `version: 2`
  `renderer: networkd`
  `ethernets:`
    `enp1s0:`
      `dhcp4: true`
After that i have connected my vm to the internet.

i ran the command
`docker compose -f generate-indexer-certs.yml run --rm generator
to get the following output. But since we are going to be using a single node deployment meaning all components is just in one stack, we are going to need to go to the directory single-node.

![[Screenshot_20251121_204052.png]]

After that im all set up for starting my wazuh. just use docker compose up -d, but in my case i need to run this in sudo. This will download the indexer manager and dashboard. After this im going to check the dashboard to make sure that its accessible.

The ip address of my soc_wazuh is 192.168.122.7!

[[Screenshot_20251121_205437.png]]