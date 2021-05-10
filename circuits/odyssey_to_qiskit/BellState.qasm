OPENQASM 2.0;
include "qelib1.inc";
qreg q3[2];
creg c3[2];
h q3[0];
id q3[1];
gate c_0_x_1_ p0,p1 {
	u3(pi/2,-pi,0) p0;
	u3(pi/2,pi,0) p1;
	cx p0,p1;
	u3(pi/2,pi,-pi) p0;
	u3(pi/2,0,0) p1;
}
c_0_x_1_ q3[1],q3[0];
measure q3[0] -> c3[1];
measure q3[1] -> c3[0];
