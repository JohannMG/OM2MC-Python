#set architecture flags
export ARCHFLAGS="-arch x86_64"
#ensure user-installed binaries take precedence 
export PATH=/usr/local/bin:$PATH
#Load .bashrc if it exsits test -f ~/.bashrc && source ~/.bashrc
