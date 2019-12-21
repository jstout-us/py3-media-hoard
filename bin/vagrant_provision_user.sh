echo "Create user directories and set paths"
mkdir -p $HOME/bin $HOME/.local/bin
echo 'PATH="/vagrant/bin:$PATH"' >> /home/$USER/.profile

echo "Cache github ssh fingerprint"
sh -c "ssh -T git@github.com -o StrictHostKeyChecking=no; true"
