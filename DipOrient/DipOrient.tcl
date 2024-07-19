# Written by Jian Zhang (jian_zhang@cug.edu.cn)
proc DipOrient {sel firstFrame lastFrame x y z} {
    proc unique_list {list} {
    array set uniq [list]
    foreach item $list {
        set uniq($item) 1
    }
    return [array names uniq]
    }
    set result [open dipz.txt w]
    set zvec [list $x $y $z]
    for { set i $firstFrame } { $i < $lastFrame } { incr i } {
        set obj [ atomselect top "$sel" frame $i ]
        puts "[expr $i-$firstFrame+1]/[expr $lastFrame - $firstFrame]"
        foreach j [ unique_list [$obj get fragment] ] {
            set dip [measure dipole [atomselect top "fragment $j" frame $i ]]
            puts $result "[expr [vecdot $zvec $dip]/[expr [veclength $zvec] * [veclength $dip]]]"
        }
    }
    close $result
}