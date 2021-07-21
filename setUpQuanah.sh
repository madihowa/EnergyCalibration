# setting XDG dir and permissions -> MIH
export XDG_RUNTIME_DIR=/lustre/scratch/madihowa/xdg
chown -R madihowa $XDG_RUNTIME_DIR
chmod -R 0700 $XDG_RUNTIME_DIR
chmod 000700 $XDG_RUNTIME_DIR 

# setting QT var -> MIH
export QT_QPA_PLATFORM='offscreen'

