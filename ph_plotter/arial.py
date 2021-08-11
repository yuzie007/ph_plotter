from matplotlib import rcParams, _mathtext

# https://qiita.com/ogose/items/d110aa090102079fe73f
_mathtext.FontConstantsBase = _mathtext.ComputerModernFontConstants

rcParams['font.family'] = 'Arial'
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'
