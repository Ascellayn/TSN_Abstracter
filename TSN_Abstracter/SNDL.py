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

class Color:
	"""SNDL-Colors Class, each color is stored as a RGB Tuple within the color type class (ie: Abyss) then followed by the name of the color (ie: Black)  
	The provided colors have the internal SNDL names:
	- Black → Arellayn
	- White → Ascellyan
	- Red → Wakamo
	- Orange → Maple
	- Yellow → Seia
	- Green → Otogi
	- Cyan → Glacier
	- Blue → Marine
	- Purple → Nebula
	- Pink → Mika"""
	class Abyss:
		"""Dark-Mode: Tertiary Color"""
		Black = (20, 0, 20);
		White = (225, 190, 225);
		Red = (105, 0, 0);
		Orange = (105, 5, 0);
		Yellow = (135, 135, 0);
		Green = (0, 135, 30);
		Cyan = (0, 130, 135);
		Blue = (10, 0, 75);
		Purple = (50, 0, 75);
		Pink = (105, 0, 105);

	class Night:
		"""Dark-Mode: Secondary Color"""
		Black = (30, 10, 30);
		White = (230, 200, 230);
		Red = (130, 5, 5);
		Orange = (130, 30, 5);
		Yellow = (155, 155, 5);
		Green = (14, 155, 40);
		Cyan = (10, 140, 155);
		Blue = (15, 0, 105);
		Purple = (75, 5, 105);
		Pink = (130, 25, 130);

	class Moon:
		"""Dark-Mode: Primary Color"""
		Black = (40, 15, 40);
		White = (235, 210, 235);
		Red = (155, 10, 10);
		Orange = (155, 55, 10);
		Yellow = (175, 175, 10);
		Green = (28, 175, 50);
		Cyan = (28, 150, 175);
		Blue = (20, 0, 135);
		Purple = (95, 10, 135);
		Pink = (155, 50, 155);

	class Sky:
		"""Light-Mode: Tertiary Color"""
		Black = (60, 25, 60);
		White = (245, 230, 245);
		Red = (205, 20, 20);
		Orange = (205, 105, 20);
		Yellow = (215, 215, 20);
		Green = (56, 215, 70);
		Cyan = (40, 170, 205);
		Blue = (30, 0, 195);
		Purple = (135, 20, 195);
		Pink = (205, 100, 205);

	class Day:
		"""Light-Mode: Secondary Color"""
		Black = (70, 30, 70);
		White = (250, 240, 250);
		Red = (230, 25, 25);
		Orange = (230, 130, 25);
		Yellow = (235, 235, 25);
		Green = (70, 240, 80);
		Cyan = (50, 180, 230);
		Blue = (35, 0, 225);
		Purple = (155, 25, 225);
		Pink = (230, 125, 230);


	class Sun:
		"""Light-Mode: Primary Color"""
		Black = (80, 35, 80);
		White = (255, 250, 255);
		Red = (255, 30, 30);
		Orange = (255, 155, 30);
		Yellow = (255, 255, 30);
		Green = (84, 255, 90);
		Cyan = (60, 190, 255);
		Blue = (40, 0, 255);
		Purple = (175, 30, 255);
		Pink = (255, 150, 255);