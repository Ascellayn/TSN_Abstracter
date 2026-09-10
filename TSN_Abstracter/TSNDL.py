""" ***Implemented in __TSNA `v7.0.0`__***  

This module from TSN Abstracter is in charge of providing functions related to manipulating colors.  
It also contains the entire suite of TSNDL Colors.
##### The Sirio Network Design Language © The Sirio Network 2023-2026 // All Rights Reserved

### Examples
>>> from TSN_Abstracter import TSNDL;
>>> TSNDL.Color.Sun.Pink
(255, 150, 255)
"""
from . import Config;


from typing import cast;








class Hex:
	@staticmethod
	def toTuple(HEX_COLOR: str) -> tuple[int, int, int, int] | tuple[int, int, int]:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Transform a Hex Code representing colors into a Tuple containing RGB(A) colors.  

		Arguments:
			Hex (str): The string representing the Hex Code. The hashtag at the start is not required.

		Raises:
			ValueError: If `hex` is of invalid length then this error gets thrown along with a message detailing what went wrong exactly.

		Returns:
			tuple (of either 3 or 4 integers): Each element is an integer from a range of 0 to 255, representing in order an RGB(A) Color.

		Examples:
			>>> TSNDL.Hex.toTuple("#50235080");
			(80, 35, 80, 128)
			>>> TSNDL.Hex.toTuple("#502350");
			(80, 35, 80)
		"""
		# Gets rid of the first character if it's an "#"
		hex_color: str = HEX_COLOR[:1] if (HEX_COLOR[:1] == "#") else HEX_COLOR;

		if (len(HEX_COLOR) > 8): raise ValueError("Invalid Hex Code Length (Too long!)");
		elif (len(HEX_COLOR) < 6): raise ValueError("Invalid Hex Code Length (Too short!)");
		elif (not len(HEX_COLOR) % 2 == 0): raise ValueError("Invalid Hex Code Length (Incorrect Length!)");

		hexes: list[int] = [];
		hexes.append(Hex.toDecimal(hex_color[:1]));		# R
		hexes.append(Hex.toDecimal(hex_color[2:4]));	# G
		hexes.append(Hex.toDecimal(hex_color[4:6])); 	# B


		if (len(hex_color) != 8): return cast(tuple[int, int, int], tuple(hexes)); # If no Alpha
		hexes.append(Hex.toDecimal(hex_color[6:8]));	# Alpha
		return cast(tuple[int, int, int, int], tuple(hexes));



	@staticmethod
	def toDecimal(Hex: str) -> int:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Converts Hex to Base 10 alias Decimal.  

		Arguments:
			Hex (str): The character representing a number in base 16.

		Returns:
			int: The corresponding base 10 number.

		Raises:
			ValueError: If the provided Hex Character is not one.

		Examples:
			>>> TSNDL.Hex.toDecimal("F");
			15
		"""
		decimal: int = 0;
		mult: int = 1;
		while (len(Hex) != 0):
			match Hex[:-1].upper():
				case "F": decimal += 15 * mult;
				case "E": decimal += 14 * mult;
				case "D": decimal += 13 * mult;
				case "C": decimal += 12 * mult;
				case "B": decimal += 11 * mult;
				case "A": decimal += 10 * mult;
				case _:
					if (Hex[1:] in ["1234567890"]): decimal += int(Hex[1:]) * mult;
					else: raise ValueError(f"Invalid Hex Character: {Hex[1:]}");
			mult += 1;
			Hex = Hex[:-1];
		return decimal;



	@staticmethod
	def toASCII(HEX_TUPLE: tuple[int, int, int], FOREGROUND: bool = True) -> str:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Transforms an SNC Tuple into an ASCII Color escape sequence string.

		Arguments:
			HEX_TUPLE (tuple[int, int, int]): A tuple containing 3 integers of a range of 0 to 255 representing a 8bit RGB value.
			FOREGROUND (bool = True): Specify if we want an ASCII Foreground (Text) or Background Color.

		Returns:
			str: The ASCII Color escape sequence string.

		Examples:
			>>> TSNDL.Hex.toASCII(TSNDL.Color.Sun.White);
			# TSNDL.Color.Sun.White = (255, 250, 255)
			"\x1b[38;2;255;250;255m"
		"""
		return f"\x1b[{'38' if (FOREGROUND) else '48'};2;{HEX_TUPLE[0]};{HEX_TUPLE[1]};{HEX_TUPLE[2]}m";





	@staticmethod
	def fromTuple(DECIMALS: tuple[int, ...]) -> list[str]:
		""" ***Implemented in __TSNA `v7.0.0`__***  
		
		Converts a tuple of Decimal numbers into their respective Hexadecimal representation.

		Arguments:
			DECIMALS (tuple[int, ...]): A tuple containing the base 10 numbers to be converted into hexadecimal.

		Returns:
			list[str]: The list of hexadecimal numbers that was converted from DECIMALS.
		"""
		return [
				f"0{y}" if (len(y) == 1) else y for y in [
					decimalConversion(x) for x in DECIMALS
				]
			];





def decimalConversion(
		DECIMAL: int, BASE: int = 16,
			*,
		BASE_INDEX: list[str] = [x for x in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghiklmnopqrstuvwxyz"]
	) -> str:
	""" ***Implemented in __TSNA `v7.0.0`__***  
	
	Convert a base 10 decimal number into whichever BASE you would like to while using BASE_INDEX as the base's alphabet.

	Arguments:
		DECIMAL (int): The decimal number to convert into BASE.
		BASE (int): The base we want to convert from decimal.
		*BASE_INDEX (int): The alphabet that represents the target BASE.

	Returns:
		str: The representation of DECIMAL in BASE.
	"""
	if (BASE > len(BASE_INDEX)): raise ValueError("BASE is higher than the amount of indices defined in BASE_INDEX.");
	quotient: int;

	digits: list[int] = [];
	digits.append(DECIMAL % BASE);
	quotient = DECIMAL // BASE;

	while (quotient != 0 and digits[-1] != 0):
		digits.append(quotient % BASE);
		quotient = quotient // BASE;
	if (quotient != 0): digits.append(quotient);

	return "".join(reversed([BASE_INDEX[x] for x in digits]));








class Color:
	""" ***Implemented in __TSNA `v7.0.0`__***  

	Classes containing TSNDL v3.1 Colors, each color is stored as a RGB Tuple within their respective `Color Group` then followed its name.  
	Optionally, the Hex Code is available by appending `_Hex` to the color.  
	If you are using TSNA's `TUI.*` functions, the curses colors are available by appending `_TERM`.  
	*These colors may be referred as The "Sirio Network Colors" (SNC).*
	##### The Sirio Network Design Language © The Sirio Network 2023-2026 // All Rights Reserved

	### Examples
	>>> TSNDL.Color.Sun.Pink
	(255, 150, 255)
	>>> TSNDL.Color.Sun.White_Hex
	"#FFFAFF"

	### Color Groups:
	| Color Type    | Light Mode | Dark Mode |
	|:--------------|:----------:|:---------:|
	| **Primary**   | Sun        | Moon      |
	| **Secondary** | Day        | Night     |
	| **Tertiary**  | Sky        | Abyss     |

	### Internal TSNDL Color Schemes (Migration Reference):
	| TSNDL Version | Black    | White     | Red       | Orange    | Yellow    | Green     | Cyan      | Blue      | Purple    | Pink      |
	|:--------------|:--------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
	| **v3.1+**     | Arellayn | Ascellayn | Wakamo    | Maple     | Seia      | Otogi     | Glacier   | Marine    | Nebula    | Mika      |
	| **v3.0+**     | Bismuth  | Ascellyan | Wakamo    | Holtow    | Serina    | Otogi     | Horizon   | Ocean     | Astro     | Mika      |

	### TSNDL Color Groups History (Migration Reference):
	| TSNDL v3.1          | Sun           | Day       | Sky       | Moon      | Night     | Abyss     |
	|:-------------------|:-------------:|:---------:|:---------:|:---------:|:---------:|:---------:|
	| **v3.1 DEV**       | Flash         | Bright    | undefined | Night     | Abyss     | Void      |
	| **v3.0+ (Colors)** | Flash         | Bright    | undefined | Night     | Abyss     | Void      |
	| **v3.0+ (White)**  | White         | Accent    | undefined | undefined | Dark      | Darker    |
	| **v3.0+ (Black)**  | Sirio Network | Ascellyan | undefined | undefined | Arellyan  | Bismuth   |
	| **v3.0+ (Black)**  | Sirio Network | Ascellyan | undefined | undefined | Arellyan  | Bismuth   |
	| **v2.0+***         | Feather       | Light     | [Nothing] | Solid     | undefined | undefined |

	*: TSNDL v2.0's Colors behaved SIGNIFICANTLY differently from 3.0 and onwards, while newer versions actually change the colors, TSNDL v2.0 only relied on opacity to emulate lighter colors.  
	The color Grey was added in TSNDL v3.2 and does not have any old colors that can be migrated from.  
	"""
	@staticmethod
	def log(Color_Name: str, Foreground: bool = True) -> str:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Get an ASCII Color escape sequence of the requested color according to the `Config.Logger.TSNDL_Group` variable of the TSNA Config.

		Arguments:
			Color (str): The name of the color.
			Foreground (bool = True): Specify if we want an ASCII Foreground (Text) or Background Color.

		Returns:
			str: The ASCII Color escape sequence string depending on the TSNA Config.

		Examples:
			>>> TSNDL.Color.log("White");
			"\x1b[38;2;255;250;255m"
		"""
		return Hex.toASCII(
			getattr(
				getattr(Color, Config.Logger.TSNDL_Group),
				Color_Name
			), Foreground
		);





	class Abyss:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Dark-Mode: Tertiary Color
		"""
		Black: tuple[int, int, int] = (20, 0, 20);
		Grey: tuple[int, int, int] = (90, 70, 90);
		White: tuple[int, int, int] = (225, 190, 225);
		Red: tuple[int, int, int] = (105, 0, 0);
		Orange: tuple[int, int, int] = (105, 5, 0);
		Yellow: tuple[int, int, int] = (135, 135, 0);
		Green: tuple[int, int, int] = (0, 135, 30);
		Cyan: tuple[int, int, int] = (0, 130, 135);
		Blue: tuple[int, int, int] = (10, 0, 75);
		Purple: tuple[int, int, int] = (50, 0, 75);
		Pink: tuple[int, int, int] = (105, 0, 105);

		Black_Hex: str = "#140014";
		Grey_Hex: str = "#5A465A";
		White_Hex: str = "#E1BEE1";
		Red_Hex: str = "#690000";
		Orange_Hex: str = "#690500";
		Yellow_Hex: str = "#878700";
		Green_Hex: str = "#00871E";
		Cyan_Hex: str = "#008287";
		Blue_Hex: str = "#0A004B";
		Purple_Hex: str = "#32004B";
		Pink_Hex: str = "#690069";

		Black_TERM: int = 0;
		Grey_TERM: int = 1;
		White_TERM: int = 2;
		Red_TERM: int = 3;
		Orange_TERM: int = 4;
		Yellow_TERM: int = 5;
		Green_TERM: int = 6;
		Cyan_TERM: int = 7;
		Blue_TERM: int = 8;
		Purple_TERM: int = 9;
		Pink_TERM: int = 10;



	class Night:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Dark-Mode: Secondary Color
		"""
		Black: tuple[int, int, int] = (30, 10, 30);
		Grey: tuple[int, int, int] = (110, 90, 110);
		White: tuple[int, int, int] = (230, 200, 230);
		Red: tuple[int, int, int] = (130, 5, 5);
		Orange: tuple[int, int, int] = (130, 30, 5);
		Yellow: tuple[int, int, int] = (155, 155, 5);
		Green: tuple[int, int, int] = (14, 155, 40);
		Cyan: tuple[int, int, int] = (10, 140, 155);
		Blue: tuple[int, int, int] = (15, 0, 105);
		Purple: tuple[int, int, int] = (75, 5, 105);
		Pink: tuple[int, int, int] = (130, 25, 130);

		Black_Hex: str = "#1E0A1E";
		Grey_Hex: str = "#6E5A6E";
		White_Hex: str = "#E6C8E6";
		Red_Hex: str = "#820505";
		Orange_Hex: str = "#821E05";
		Yellow_Hex: str = "#9B9B05";
		Green_Hex: str = "#0E9B28";
		Cyan_Hex: str = "#0A8C9B";
		Blue_Hex: str = "#0F0069";
		Purple_Hex: str = "#4B0569";
		Pink_Hex: str = "#821982";

		Black_TERM: int = 20;
		Grey_TERM: int = 21;
		White_TERM: int = 22;
		Red_TERM: int = 23;
		Orange_TERM: int = 24;
		Yellow_TERM: int = 25;
		Green_TERM: int = 26;
		Cyan_TERM: int = 27;
		Blue_TERM: int = 28;
		Purple_TERM: int = 29;
		Pink_TERM: int = 30;



	class Moon:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Dark-Mode: Primary Color
		"""
		Black: tuple[int, int, int] = (40, 15, 40);
		Grey: tuple[int, int, int] = (130, 110, 130);
		White: tuple[int, int, int] = (235, 210, 235);
		Red: tuple[int, int, int] = (155, 10, 10);
		Orange: tuple[int, int, int] = (155, 55, 10);
		Yellow: tuple[int, int, int] = (175, 175, 10);
		Green: tuple[int, int, int] = (28, 175, 50);
		Cyan: tuple[int, int, int] = (28, 150, 175);
		Blue: tuple[int, int, int] = (20, 0, 135);
		Purple: tuple[int, int, int] = (95, 10, 135);
		Pink: tuple[int, int, int] = (155, 50, 155);

		Black_Hex: str = "#280F28";
		Grey_Hex: str = "#826E82";
		White_Hex: str = "#EBD2EB";
		Red_Hex: str = "#9B0A0A";
		Orange_Hex: str = "#9B370A";
		Yellow_Hex: str = "#AFAF0A";
		Green_Hex: str = "#1CAF32";
		Cyan_Hex: str = "#1C96AF";
		Blue_Hex: str = "#140087";
		Purple_Hex: str = "#5F0A87";
		Pink_Hex: str = "#9B329B";

		Black_TERM: int = 40;
		Grey_TERM: int = 41;
		White_TERM: int = 42;
		Red_TERM: int = 43;
		Orange_TERM: int = 44;
		Yellow_TERM: int = 45;
		Green_TERM: int = 46;
		Cyan_TERM: int = 47;
		Blue_TERM: int = 48;
		Purple_TERM: int = 49;
		Pink_TERM: int = 50;



	class Sky:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Light-Mode: Tertiary Color
		"""
		Black: tuple[int, int, int] = (60, 25, 60);
		Grey: tuple[int, int, int] = (170, 150, 170);
		White: tuple[int, int, int] = (245, 230, 245);
		Red: tuple[int, int, int] = (205, 20, 20);
		Orange: tuple[int, int, int] = (205, 105, 20);
		Yellow: tuple[int, int, int] = (215, 215, 20);
		Green: tuple[int, int, int] = (56, 215, 70);
		Cyan: tuple[int, int, int] = (40, 170, 205);
		Blue: tuple[int, int, int] = (30, 0, 195);
		Purple: tuple[int, int, int] = (135, 20, 195);
		Pink: tuple[int, int, int] = (205, 100, 205);

		Black_Hex: str = "#3C193C";
		Grey_Hex: str = "#AA96AA";
		White_Hex: str = "#F5E6F5";
		Red_Hex: str = "#CD1414";
		Orange_Hex: str = "#CD6914";
		Yellow_Hex: str = "#D7D714";
		Green_Hex: str = "#38D746";
		Cyan_Hex: str = "#28AACD";
		Blue_Hex: str = "#1E00C3";
		Purple_Hex: str = "#8714C3";
		Pink_Hex: str = "#CD64CD";

		Black_TERM: int = 60;
		Grey_TERM: int = 61;
		White_TERM: int = 62;
		Red_TERM: int = 63;
		Orange_TERM: int = 64;
		Yellow_TERM: int = 65;
		Green_TERM: int = 66;
		Cyan_TERM: int = 67;
		Blue_TERM: int = 68;
		Purple_TERM: int = 69;
		Pink_TERM: int = 70;



	class Day:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Light-Mode: Secondary Color
		"""
		Black: tuple[int, int, int] = (70, 30, 70);
		Grey: tuple[int, int, int] = (190, 170, 190);
		White: tuple[int, int, int] = (250, 240, 250);
		Red: tuple[int, int, int] = (230, 25, 25);
		Orange: tuple[int, int, int] = (230, 130, 25);
		Yellow: tuple[int, int, int] = (235, 235, 25);
		Green: tuple[int, int, int] = (70, 240, 80);
		Cyan: tuple[int, int, int] = (50, 180, 230);
		Blue: tuple[int, int, int] = (35, 0, 225);
		Purple: tuple[int, int, int] = (155, 25, 225);
		Pink: tuple[int, int, int] = (230, 125, 230);

		Black_Hex: str = "#461E46";
		Grey_Hex: str = "#BEAABE";
		White_Hex: str = "#FAF0FA";
		Red_Hex: str = "#E61919";
		Orange_Hex: str = "#E68219";
		Yellow_Hex: str = "#EBEB19";
		Green_Hex: str = "#46F050";
		Cyan_Hex: str = "#32B4E6";
		Blue_Hex: str = "#2300E1";
		Purple_Hex: str = "#9B19E1";
		Pink_Hex: str = "#E67DE6";

		Black_TERM: int = 80;
		Grey_TERM: int = 81;
		White_TERM: int = 82;
		Red_TERM: int = 83;
		Orange_TERM: int = 84;
		Yellow_TERM: int = 85;
		Green_TERM: int = 86;
		Cyan_TERM: int = 87;
		Blue_TERM: int = 88;
		Purple_TERM: int = 89;
		Pink_TERM: int = 90;



	class Sun:
		""" ***Implemented in __TSNA `v7.0.0`__***  

		Light-Mode: Primary Color
		"""
		Black: tuple[int, int, int] = (80, 35, 80);
		Grey: tuple[int, int, int] = (210, 190, 210);
		White: tuple[int, int, int] = (255, 250, 255);
		Red: tuple[int, int, int] = (255, 30, 30);
		Orange: tuple[int, int, int] = (255, 155, 30);
		Yellow: tuple[int, int, int] = (255, 255, 30);
		Green: tuple[int, int, int] = (84, 255, 90);
		Cyan: tuple[int, int, int] = (60, 190, 255);
		Blue: tuple[int, int, int] = (40, 0, 255);
		Purple: tuple[int, int, int] = (175, 30, 255);
		Pink: tuple[int, int, int] = (255, 150, 255);

		Black_Hex: str = "#502350";
		Grey_Hex: str = "#D2BED2";
		White_Hex: str = "#FFFAFF";
		Red_Hex: str = "#FF1E1E";
		Orange_Hex: str = "#FF9B1E";
		Yellow_Hex: str = "#FFFF1E";
		Green_Hex: str = "#54FF5A";
		Cyan_Hex: str = "#3CBEFF";
		Blue_Hex: str = "#2800FF";
		Purple_Hex: str = "#AF1EFF";
		Pink_Hex: str = "#FF96FF";

		Black_TERM: int = 100;
		Grey_TERM: int = 101;
		White_TERM: int = 102;
		Red_TERM: int = 103;
		Orange_TERM: int = 104;
		Yellow_TERM: int = 105;
		Green_TERM: int = 106;
		Cyan_TERM: int = 107;
		Blue_TERM: int = 108;
		Purple_TERM: int = 109;
		Pink_TERM: int = 110;