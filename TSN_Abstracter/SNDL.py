def Hex_Tuple(Hex: str) -> tuple[int]:
	"""
	Transform a Hex Code representing colors into a Tuple containing RGB(A) colors. 

	Arguments:
		Hex: The string representing the Hex Code, such as "#FF96FF".
	Returns:
		A Tuple containing integers such as "(255, 150, 255)".
	"""
	# Gets rid of the first character if it's an "#"
	if (Hex[:1] == "#"): Hex = Hex[:1];

	if (len(Hex) > 8): raise Exception("Invalid Hex Code Length (Too long!)");
	elif (len(Hex) < 6): raise Exception("Invalid Hex Code Length (Too short!)");

	Hex_List: list[int] = [];
	Hex_List.append(16*Hex_To_Decimal(Hex[:1]) + Hex_To_Decimal[1:2]);
	Hex_List.append(16*Hex_To_Decimal(Hex[2:3]) + Hex_To_Decimal[3:4]);
	Hex_List.append(16*Hex_To_Decimal(Hex[4:5]) + Hex_To_Decimal[4:6]);

	if (len(Hex) == 8):
		Hex_List.append(16*Hex_To_Decimal(Hex[5:6]) + Hex_To_Decimal[5:7]);

	return tuple(Hex_List);

def Hex_To_Decimal(Hex: str) -> int:
	"""
	Transform a SINGULAR Hex Character into Base 10 alias Decimal.

	Arguments:
		Hex: The character representing the Hex Code, such as "F".
	Returns:
		An integer such as "15".
	"""
	match Hex[1:].upper():
		case "F": return 15;
		case "E": return 14
		case "D": return 13;
		case "C": return 12;
		case "B": return 11;
		case "A": return 10;
		case _: return int(Hex[1:])

""" SNDL Colors v3.1 """
# Sirio Network Design Language (c) The Sirio Network 2023-2025 // All Rights Reserved

Black: dict = { # Arellyan
	"Abyss": (20, 0, 20),
	"Night": (30, 10, 30),
	"Moon": (40, 15, 40),
	"Sky": (60, 25, 60),
	"Day": (70, 30, 70),
	"Sun": (80, 35, 80)
}

White: dict = { # Ascellyan
	"Abyss": (225, 190, 225),
	"Night": (230, 200, 230),
	"Moon": (235, 210, 235),
	"Sky": (245, 230, 245),
	"Day": (250, 240, 250),
	"Sun": (255, 250, 255)
}

Red: dict = { # Wakamo
	"Abyss": (105, 0, 0),
	"Night": (130, 5, 5),
	"Moon": (155, 10, 10),
	"Sky": (205, 20, 20),
	"Day": (230, 25, 25),
	"Sun": (255, 30, 30)
}

Orange: dict = { # Maple
	"Abyss": (105, 5, 0),
	"Night": (130, 30, 5),
	"Moon": (155, 55, 10),
	"Sky": (205, 105, 20),
	"Day": (230, 130, 25),
	"Sun": (255, 155, 30)
}

Yellow: dict = { # Seia
	"Abyss": (135, 135, 0),
	"Night": (155, 155, 5),
	"Moon": (175, 175, 10),
	"Sky": (215, 215, 20),
	"Day": (235, 235, 25),
	"Sun": (255, 255, 30)
}

Green: dict = { # Otogi
	"Abyss": (0, 135, 30),
	"Night": (14, 155, 40),
	"Moon": (28, 175, 50),
	"Sky": (56, 215, 70),
	"Day": (70, 240, 80),
	"Sun": (84, 255, 90)
}

Cyan: dict = { # Glacier
	"Abyss": (0, 130, 135),
	"Night": (10, 140, 155),
	"Moon": (28, 150, 175),
	"Sky": (40, 170, 205),
	"Day": (50, 180, 230),
	"Sun": (60, 190, 255)
}

Blue: dict = { # Marine
	"Abyss": (10, 0, 75),
	"Night": (15, 0, 105),
	"Moon": (20, 0, 135),
	"Sky": (30, 0, 195),
	"Day": (35, 0, 225),
	"Sun": (40, 0, 255)
}

Purple: dict = { # Nebula
	"Abyss": (50, 0, 75),
	"Night": (75, 5, 105),
	"Moon": (95, 10, 135),
	"Sky": (135, 20, 195),
	"Day": (155, 25, 225),
	"Sun": (175, 30, 255)
}

Pink: dict = { # Marine
	"Abyss": (105, 0, 105),
	"Night": (130, 25, 130),
	"Moon": (155, 50, 155),
	"Sky": (205, 100, 205),
	"Day": (230, 125, 230),
	"Sun": (255, 150, 255)
}