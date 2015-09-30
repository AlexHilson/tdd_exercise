# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000,
    auto_correct: true

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3-pip xvfb firefox
    sudo pip3 install django==1.8
    sudo pip3 install --upgrade selenium
    sudo pip3 install virtualenv
    
    Xvfb :99&
    echo "export DISPLAY=:99" >> ~/.profile
  SHELL
end
