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
		Black = (20, 0, 20);		#140014
		White = (225, 190, 225);	#E1BEE1
		Red = (105, 0, 0);			#690000
		Orange = (105, 5, 0);		#690500
		Yellow = (135, 135, 0);		#878700
		Green = (0, 135, 30);		#00871E
		Cyan = (0, 130, 135);		#008287
		Blue = (10, 0, 75);			#0A004B
		Purple = (50, 0, 75);		#32004B
		Pink = (105, 0, 105);		#690069

	class Night:
		"""Dark-Mode: Secondary Color"""
		Black = (30, 10, 30);		#1E0A1E
		White = (230, 200, 230);	#E6C8E6
		Red = (130, 5, 5);			#820505
		Orange = (130, 30, 5);		#821E05
		Yellow = (155, 155, 5);		#9B9B05
		Green = (14, 155, 40);		#0E9B28
		Cyan = (10, 140, 155);		#0A8C9B
		Blue = (15, 0, 105);		#0F0069
		Purple = (75, 5, 105);		#4B0569
		Pink = (130, 25, 130);		#821982

	class Moon:
		"""Dark-Mode: Primary Color"""
		Black = (40, 15, 40);		#280F28
		White = (235, 210, 235);	#EBD2EB
		Red = (155, 10, 10);		#9B0A0A
		Orange = (155, 55, 10);		#9B370A
		Yellow = (175, 175, 10);	#AFAF0A
		Green = (28, 175, 50);		#1CAF32
		Cyan = (28, 150, 175);		#1C96AF
		Blue = (20, 0, 135);		#140087
		Purple = (95, 10, 135);		#5F0A87
		Pink = (155, 50, 155);		#9B329B

	class Sky:
		"""Light-Mode: Tertiary Color"""
		Black = (60, 25, 60);		#3C193C
		White = (245, 230, 245);	#F5E6F5
		Red = (205, 20, 20);		#CD1414
		Orange = (205, 105, 20);	#CD6914
		Yellow = (215, 215, 20);	#D7D714
		Green = (56, 215, 70);		#38D746
		Cyan = (40, 170, 205);		#28AACD
		Blue = (30, 0, 195);		#1E00C3
		Purple = (135, 20, 195);	#8714C3
		Pink = (205, 100, 205);		#CD64CD

	class Day:
		"""Light-Mode: Secondary Color"""
		Black = (70, 30, 70);		#461E46
		White = (250, 240, 250);	#FAF0FA
		Red = (230, 25, 25);		#E61919
		Orange = (230, 130, 25);	#E68219
		Yellow = (235, 235, 25);	#EBEB19
		Green = (70, 240, 80);		#46F050
		Cyan = (50, 180, 230);		#32B4E6
		Blue = (35, 0, 225);		#2300E1
		Purple = (155, 25, 225);	#9B19E1
		Pink = (230, 125, 230);		#E67DE6


	class Sun:
		"""Light-Mode: Primary Color"""
		Black = (80, 35, 80);		#502350
		White = (255, 250, 255);	#FFFAFF
		Red = (255, 30, 30);		#FF1E1E
		Orange = (255, 155, 30);	#FF9B1E
		Yellow = (255, 255, 30);	#FFFF1E
		Green = (84, 255, 90);		#54FF5A
		Cyan = (60, 190, 255);		#3CBEFF
		Blue = (40, 0, 255);		#2800FF
		Purple = (175, 30, 255);	#AF1EFF
		Pink = (255, 150, 255);		#FF96FF