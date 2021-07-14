# lammpsHT
A python package way for systematically running lammps simulation (or any scientific software) in a high throughput manner

The information required to generate the automization code
=================================================================================================================================
Filename lammps.in
N_layers 2

N = 1 START

    N_ensemble 5
    cores 4
    njobs 5
    use_template 0

    PRE 
        mkdir results
    END pre


    Line id1 1
        index 1
        parameter random
    END line

    Line id2 1
        index 3
        parameter random
    END line

    Line id3 1
        index 4
        parameter random
    END line


    POST
        calculate.py --output result_{k}
        mv result_* results
    END post
    
END layer

N = 2 START
    njobs 1
    Line pressure 1
        index 5
        parameter [-0.1, -1.0, -1.5, -2, -2.5, -3] 
    END line
    
END layer
=================================================================================================================================

