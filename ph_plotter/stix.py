from matplotlib import rcParams, mathtext, font_manager
from matplotlib.font_manager import FontProperties

del font_manager.weight_dict['roman']
font_manager._rebuild()

# https://github.com/matplotlib/matplotlib/pull/3912
fp = FontProperties(fname='/System/Library/Fonts/Supplemental/STIXGeneral.otf')

# https://qiita.com/ogose/items/d110aa090102079fe73f
mathtext.FontConstantsBase = mathtext.ComputerModernFontConstants

rcParams['font.family'] = fp.get_name()
rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.rm'] = 'stix'
rcParams['mathtext.it'] = 'stix:italic'
rcParams['mathtext.bf'] = 'stix:bold'
