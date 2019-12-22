# -*- mode: ruby -*-
# vi: set ft=ruby :

DEV_CFG_ROOT = ENV["DEV_CFG_ROOT"]

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 4
  end

  config.ssh.forward_agent = true
  config.vm.hostname = "media-hoard"
  config.vm.provision "file", source: "#{DEV_CFG_ROOT}/locations/jstout-us/gitconfig",
                              destination: ".gitconfig",
                              run: "always"
  config.vm.provision "file", source: "#{DEV_CFG_ROOT}/locations/jstout-us/pypi_invoke.yaml",
                              destination: ".invoke.yaml",
                              run: "always"
  config.vm.provision "shell", path: "bin/vagrant_provision.sh"
  config.vm.provision "shell", path: "bin/vagrant_provision_user.sh", privileged: false
end
