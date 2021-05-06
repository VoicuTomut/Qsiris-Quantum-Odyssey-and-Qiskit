OPENQASM 2.0;
include "qelib1.inc";
qreg q0[2];
creg c0[2];
x q0[0];
id q0[1];
gate c_0_h_1_ p0,p1 {
	u3(3*pi/4,0,-2*pi) p0;
	u3(pi/2,2*pi,0) p1;
	cx p0,p1;
	u3(3*pi/4,pi,-pi) p0;
	u3(pi/2,0,pi) p1;
}
c_0_h_1_ q0[1],q0[0];
measure q0[0] -> c0[1];
measure q0[1] -> c0[0];
