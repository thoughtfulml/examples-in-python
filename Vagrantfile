# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python python-nose-parameterized python-numpy python-sklearn python-pip python-bs4 python-pandas
    pip install --upgrade pip
    pip install theanets
    apt-get install -y python3 python3-nose-parameterized python3-numpy python3-sklearn python3-pip python3-bs4 python3-pandas
    pip3 install --upgrade pip
    pip3 install theanets
  SHELL
end
