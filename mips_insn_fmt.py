# @author topcue

# todo:
# negative integer
# ex) [bne  $4, $0, -4] -> [bne $r0, $a0, 262140] (wrong)


# https://en.wikibooks.org/wiki/MIPS_Assembly/Instruction_Formats
INSTRUCTIONS_TABLE = [
	['Mnemonic', 'Opcode', 'Funct', 'Type'],
	['addi', '0x08', 'NA', 'I'],
	['addiu', '0x09', 'NA', 'I'],
	['andi', '0x0C', 'NA', 'I'],
	['beq', '0x04', 'NA', 'I'],
	['blez', '0x06', 'NA', 'I'],
	['bne', '0x05', 'NA', 'I'],
	['bgtz', '0x07', 'NA', 'I'],
	['lb', '0x20', 'NA', 'I'],
	['lbu', '0x24', 'NA', 'I'],
	['lhu', '0x25', 'NA', 'I'],
	['lui', '0x0F', 'NA', 'I'],
	['lw', '0x23', 'NA', 'I'],
	['ori', '0x0D', 'NA', 'I'],
	['sb', '0x28', 'NA', 'I'],
	['sh', '0x29', 'NA', 'I'],
	['slti', '0x0A', 'NA', 'I'],
	['sltiu', '0x0B', 'NA', 'I'],
	['sw', '0x2B', 'NA', 'I'],
	['j', '0x02', 'NA', 'J'],
	['jal', '0x03', 'NA', 'J'],
	['jalr', '0x00', '0x09', 'J'],
	['add', '0x00', '0x20', 'R'],
	['addu', '0x00', '0x21', 'R'],
	['and', '0x00', '0x24', 'R'],
	['div', '0x00', '0x1A', 'R'],
	['divu', '0x00', '0x1B', 'R'],
	['jr', '0x00', '0x08', 'R'],
	['mfhi', '0x00', '0x10', 'R'],
	['mthi', '0x00', '0x11', 'R'],
	['mflo', '0x00', '0x12', 'R'],
	['mtlo', '0x00', '0x13', 'R'],
	['mfc0', '0x10', 'NA', 'R'],	# TODO;
	['mult', '0x00', '0x18', 'R'],
	['multu', '0x00', '0x19', 'R'],
	['nor', '0x00', '0x27', 'R'],
	['xor', '0x00', '0x26', 'R'],
	['or', '0x00', '0x25', 'R'],
	['slt', '0x00', '0x2A', 'R'],
	['sltu', '0x00', '0x2B', 'R'],
	['sll', '0x00', '0x00', 'R'],
	['srl', '0x00', '0x02', 'R'],
	['sra', '0x00', '0x03', 'R'],
	['sub', '0x00', '0x22', 'R'],
	['subu', '0x00', '0x2', 'R']
]

REGISTERS = [
	'r0', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 
	't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
	's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7',
	't8', 't9', 'k0', 'k1', 'gp', 'sp', 's8', 'ra'
]

def b2h(b, n="02X"):
	return "0x" + format(int(b, 2), n)

def b2d(b):
	return str(int(b, 2))

def rr(r):
	return REGISTERS[int(r)]

def show_bin_str(s):
	print("\n\n[+]", s)
	print("    ", end='')
	for i in range(0, 32, 4):
		print(s[i:i+4] + ' ', end='')
	print()


def get_format(s):
	op = b2h(s[0:6])
	funct = b2h(s[-6:])

	if (op in ("0x02", "0x03")) or (op == "0x00" and funct == "0x09"):
			return "J"
	if (op == "0x00") or (op == "0x10"):
		return "R"
	else:
		return "I"


def parse_R_format(s):
	op = b2h(s[0:6])
	funct = b2h(s[-6:])
	

	if op == "0x00":
		for insn in INSTRUCTIONS_TABLE:
			if insn[2] == funct:
				break
	else:	# op == "0x10"
		for insn in INSTRUCTIONS_TABLE:
			if insn[0] == "mfc0":
				break

	mnemonic, op, funct, fmt = insn
	op, rs, rt, rd, shamt, funct = s[0:6], s[6:11], s[11:16], s[16:21], s[21:26], s[-6:]

	show_bin_str(s)
	print("\n    [{} ${}, ${}, ${}]".format(mnemonic, rr(b2d(rd)), rr(b2d(rs)), rr(b2d(rt))), end=" ")
	print(fmt + "-Format")
	print("    op     rs    rt    rd    shamt funct")
	print("   ", op, rs, rt, rd, shamt, funct)
	print("    {}   {}  {}  {}  {}  {}".format(b2h(op), b2h(rs), b2h(rt), b2h(rd), b2h(shamt), b2h(funct)))


def parse_I_format(s):
	op = b2h(s[0:6])

	for insn in INSTRUCTIONS_TABLE:
		if insn[1] == op:
			break

	mnemonic, op, funct, fmt = insn
	op, rs, rt, imm = s[0:6], s[6:11], s[11:16], s[16:]

	show_bin_str(s)
	print_imm = imm + '00' if (mnemonic[:1] == 'b') else imm
	print("\n    [{} ${}, ${}, {}]".format(mnemonic, rr(b2d(rt)), rr(b2d(rs)), b2d(print_imm)), end=" ")
	print(fmt + "-Format")
	print("    op     rs    rt    imm")
	print("   ", op, rs, rt, imm)
	print("    {}   {}  {}  {}".format(b2h(op), b2h(rs), b2h(rt), b2h(imm, "04X")))


def parse_J_format(s):
	op = b2h(s[0:6])

	if op == "0x02":
		mn = "j"
	elif op == "0x03":
		mn = "jal"
	elif op == "0x00":
		mn = "jalr"

	for insn in INSTRUCTIONS_TABLE:
		if insn[0] == mn:
			break

	mnemonic, op, funct, fmt = insn
	op, addr = s[0:6], s[6:]

	show_bin_str(s)
	print("\n    [{} {}]".format(mnemonic, b2h(addr+"00")), end=" ")
	print(fmt + "-Format")
	print("    op addr")
	print("   ", op, addr)
	print("    {}   {}".format(b2h(op), b2h(addr)))


def parse(insn):
	bin_str = format(insn, "032b")
	
	fmt = get_format(bin_str)

	if fmt == "R":
		parse_R_format(bin_str)
	elif fmt == "I":
		parse_I_format(bin_str)
	elif fmt == "J":
		parse_J_format(bin_str)


def main():	
	arr = [0x3c101001, 0x20110005, 0x00004020, 0x00009020, 0x0111482a, 0x11200006, 0x8e0a0000, 0x024a9020, 0x21080001, 0x22100004, 0x0810000d, 0x03e00008]

	# for insn in arr:
	# 	parse(insn)

	parse(0x1480ffff)
	parse(0x0c100045)


if __name__ == "__main__":
	main()


# EOF
