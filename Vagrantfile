Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.hostname = "idp"
  config.vm.network "private_network", ip: "10.11.12.99"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
    vb.name = config.vm.hostname
  end  # each vb

  config.vm.provision "shell", inline: <<-SHELL
    mkdir /root/.ssh
    chmod 700 /root/.ssh
    cat /vagrant/files/ssh/idp_rsa.pub >> /root/.ssh/authorized_keys
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    apt -y update
    apt install -y python-minimal
  SHELL

end

