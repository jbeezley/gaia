# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  host_port = ENV["GIRDER_HOST_PORT"] || 8080
  sync_folders = ENV["DEVELOPMENT_SYNC_FOLDERS"] || false

  config.vm.network "forwarded_port", guest: 8080, host: host_port

  config.vm.define "gaiavagrant" do |node| end

  config.vm.provider "virtualbox" do |vb|
    host = RbConfig::CONFIG['host_os']

    # Give VM 1/4 system memory & access to 1/2 of the cpu cores on the host
    if host =~ /darwin/
      cpus = `sysctl -n hw.ncpu`.to_i
      cpus = cpus / 4
      # sysctl returns Bytes and we need to convert to MB
      mem = `sysctl -n hw.memsize`.to_i / 1024 / 1024 / 4
    elsif host =~ /linux/
      cpus = `nproc`.to_i
      cpus = cpus / 2
      # meminfo shows KB and we need to convert to MB
      mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i / 1024 / 4
    else # Guess!
      cpus = 2
      mem = 4096
    end

    vb.customize ["modifyvm", :id, "--memory", mem]
    vb.customize ["modifyvm", :id, "--cpus", cpus]
    vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]

  end

  config.vm.synced_folder ".", "/vagrant", disabled: true

  if sync_folders
    # This is experimental and intended for developers who are
    # working directly on code in the virtualized instance,
    # no support, warranty or ganuntee of correctness!
    GIRDER_UID = GIRDER_GID = 1002
    config.vm.synced_folder ".", "/opt/gaia", owner: GIRDER_UID, group: GIRDER_GID
  end


  ansible_tags = ENV["VAGRANT_ANSIBLE_TAGS"] || false

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "vv"

    if ansible_tags
        ansible.tags = ansible_tags
    end

    ansible.groups = {
      "all" => ['gaiavagrant'],
      "girder" => ['gaiavagrant'],
      "mongo" => ['gaiavagrant'],
      "rabbitmq" => ['gaiavagrant']
    }

    ansible.extra_vars = {
      default_user: "vagrant"
    }

    ansible.playbook = "ansible/site.yml"
  end
end
