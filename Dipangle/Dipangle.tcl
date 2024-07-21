# Written by Jian Zhang (jian_zhang@cug.edu.cn)
# Last update: 2024-Jul-21 
proc Dipangle {selIon dist_1 dist_2} {
    set n [ molinfo top get numframes ]
    set result [open dip.txt w]
    for { set i 0 } { $i < $n } { incr i } {
        set ion [ atomselect top "$selIon" frame $i ]
        puts "[expr $i+1]/$n"
        foreach j [$ion list] {
            set singleion [atomselect top "index $j" frame $i]
            set wa [ atomselect top "{not same residue as {exwithin $dist_1 of index $j }} \
            and name OW and same residue as {exwithin $dist_2 of index $j}" frame $i]
            foreach m [$wa get resid] {
                set dip [measure dipole [atomselect top "resid $m" frame $i ]]
                set ow [atomselect top "resid $m and name OW" frame $i ]
                set vec [list [expr [$singleion get x] - [$ow get x]] \
                [expr [$singleion get y] - [$ow get y]] [expr [$singleion get z] - [$ow get z]]]
                puts $result "[expr [vecdot $vec $dip]/[expr [veclength $vec] * [veclength $dip]]]"
            }
        }
    }
    close $result
}

