# A script to calculate  number of ions passing through the membrane in MD by VMD
# Written by Jian Zhang (jian_zhang@cug.edu.cn)
# Version: 20240517
#################################################
# file_1: .gro
# file_2: .xtc
# direction: x/y/z/X/Y/Z
# firstFrame: an integer, specifies the first frame ID
# lastFrame: an integer, specifies the last frame ID
# ionSelection: specify the ions that pass through the membrane, using VMD atom selection syntax
# membrSelection: specify the membrane, using VMD atom selection syntax
# skip: frequency of data output, default: 1
# fn: output file name, default: result.txt
proc accromem {file_1 file_2 direction firstFrame lastFrame ionSelection membrSelection {skip 1} {fn "result.txt"}} {
    
    # import files
    mol new $file_1
    mol addfile $file_2 first $firstFrame last $lastFrame waitfor all
    set flag 0

    # determine the direction
    if {[string equal -nocase $direction x]} {
            set flag 1
            puts "The direction of ions through membrane: X"
    } elseif {[string equal -nocase $direction y]} {
            set flag 2
            puts "The direction of ions through membrane: Y"
    } elseif {[string equal -nocase $direction z]} {
            set flag 3
            puts "The direction of ions through membrane: Z"
    } else {
        puts "Please check the direction of ions through membrane"
        exit 0
    }

   
    
    # determine if parameters of firstFrame and lastFrame are reasonable
    set nFrame [molinfo top get numframes]
    if { !($firstFrame >= 0 && $lastFrame > 0 && $lastFrame > $firstFrame && $lastFrame <= $nFrame) } {
        puts "Please check firstFrame and lastFrame parameters"
        exit 0
    }

    set result [open $fn w]

    # Calculate the number of ions passing through the membrane
    set ion_pass 0
    for {set f $firstFrame} {$f<[expr {$lastFrame-1}]} {incr f} {
        puts "progress: [expr {$f+1}] / [expr {$lastFrame-$firstFrame}]"
        set ion [atomselect top "$ionSelection" frame $f]
        set membr_1 [atomselect top "$membrSelection" frame $f]
        set membr_2 [atomselect top "$membrSelection" frame {expr [$f+1]}]
        foreach i [$ion list] {
            if {$flag==1} {
                if {[[atomselect top "index $i" frame $f] get x] <= [lindex [measure minmax $membr_1] 1 0] \
                && [[atomselect top "index $i" frame [expr {$f+1}]] get x] >= [lindex [measure minmax $membr_2] 1 0]} {
                    incr ion_pass
                }
                } elseif {$flag==2} {
                if {[[atomselect top "index $i" frame $f] get y] <= [lindex [measure minmax $membr_1] 1 1] \
                && [[atomselect top "index $i" frame [expr {$f+1}]] get y] >= [lindex [measure minmax $membr_2] 1 1]} {
                    incr ion_pass
                }
                } elseif {$flag==3} {
                if {[[atomselect top "index $i" frame $f] get z] <= [lindex [measure minmax $membr_1] 1 2] \
                && [[atomselect top "index $i" frame [expr {$f+1}]] get z] >= [lindex [measure minmax $membr_2] 1 2]} {
                    incr ion_pass
                }
                }
            }
        $ion delete 
        $membr_1 delete 
        $membr_2 delete
        
	if {[expr [expr $f+1]%$skip ]==0} {
	    puts $result "[expr $f+1] $ion_pass"
    }
}
close $result 
puts "The number of ions passing through the membrane is $ion_pass"
}









