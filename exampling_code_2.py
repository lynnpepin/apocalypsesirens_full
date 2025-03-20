"""
These are just notes about interacting with an image through Gimp-Fu!

Parts to finish here:
1. Do over all CSVs
2. Optional export to xcf
3. Info box
4. Documentation
"""

def read_line(headers, line, sep="§"):
    """
    :param headers: List of string, Headers of a CSV
    :param line:    List of 
    :param sep:
    
    :returns: Dict of string --> value
    
    >>> read_line(['width', 'height', 'shape'], '3.0, 2.0, rectangle', 'n')
    {'width' : '3.0', 'height' : '2.0', 'shape' : 'rectangle'}
    """
    return {key : value.strip()
            for key, value in zip(headers, line.strip().split(sep))}

def read_csv(fn = "cards.csv", sep="§", linesep="\n"):
    """
    :param fn:      String, filename of CSV to read.
    :param sep:     String, value separator for given CSV
    :param linesep: String, line seperator for given CSV.
    
    :returns: List of dict, representing said CSV
    """
    with open(fn, "r") as ff:
        lines = ff.read().strip().split(linesep)
        headers = lines[0].strip().split(sep)
        output = [read_line(headers, line, sep=sep) for line in lines[1:]]
    
    return output


def make(title_text     = 'DOCTOR TOOTS 300000',
         card_level     = 3,
         art_asset_fn   = b'assets/art_1.png',
         out_fn         = b'out_1.png',
         max_title_len  = 200,
         source_fn      = b'example.xcf',
         root_dir       = b'/home/lynn/proj/apocalypse_sirens/small_example/'):
    """
    :param title_text:      String, text of card title
    :param card_level:      Int,    number of pips to show on card
    :param art_asset_fn:    String, filename locating the cards art asset
    :param out_fn:          String, filename to export card to
    :param max_title_len:   Int,    max number of pixels wide the title can be
        (Title is squished to fit the length)
    :param source_fn:       String, the XCF file to base this off of.
    :param root_dir:        String, the root directory to look for things at.
    """
    # TODO: Break this up into smaller functions?
    
    # 1. Load xcf
    img = pdb.gimp_xcf_load(0, root_dir + source_fn, root_dir + source_fn)
    
    # 2. Set Title Text
    # img = gimp.image_list()[0]
    # This layer should be named 'Title', and should be set to 'Dynamic'
    title_layer = pdb.gimp_image_get_layer_by_name(img, 'Title')
    pdb.gimp_text_layer_set_text(title_layer, title_text)
    
    # Resize Title layer if it is long
    # (Note: Layer must be set 'dynamic', not fixed)
    curr_width = pdb.gimp_drawable_width(title_layer)
    
    # Iteratively squeeze the text
    while curr_width > max_title_len:
        pdb.gimp_text_layer_set_letter_spacing(title_layer,
            pdb.gimp_text_layer_get_letter_spacing(title_layer) - 0.2)
        
        curr_width = pdb.gimp_drawable_width(title_layer)
        # Consider: Don't let spacing get < some size;
        # once spacing hits -4.0, start reducing font size or something?
    
    # Create title dropshadow
    title_copy = title_layer.copy(False)
    pdb.gimp_image_set_active_layer(img, title_layer)
    img.add_layer(title_copy)
    pdb.gimp_image_lower_layer(img, title_copy)
    pdb.gimp_layer_resize_to_image_size(title_copy)
    pdb.gimp_drawable_invert(title_copy, 1)
    pdb.plug_in_gauss_iir(img, title_copy, 6.0, 4, 4)
    pdb.gimp_drawable_levels(title_copy, 4, 0.0, 0.5, False, 1.0, 0.0, 1.0, False)
    
    # TODO: Set info here!
    
    # 2. Set levels, represented as pips (a-la Yu-Gi-Oh)
    # We have 4 layers, titled 'Level_1', ..., 'Level_2'
    # We set up to 4 of them visible here.
    level_layers = [pdb.gimp_image_get_layer_by_name(img, 'Level_' + str(x)) for x in [1, 2, 3, 4]]
    for level_layer in level_layers:
        pdb.gimp_item_set_visible(level_layer, False)
    
    for ii in range(int(card_level)):
        pdb.gimp_item_set_visible(level_layers[ii], True)
    
    # set art
    art_layer = pdb.gimp_file_load_layer(img, root_dir + art_asset_fn)
    img.add_layer(art_layer)
    
    # raise layer above the bottom
    pdb.gimp_image_lower_item_to_bottom(img, art_layer)
    pdb.gimp_image_raise_item(img, art_layer)
    
    pdb.gimp_image_merge_visible_layers(img, 1)
    drw = pdb.gimp_image_get_active_drawable(img)
    pdb.gimp_edit_copy_visible(img)
    pdb.file_png_save(img, drw, root_dir + out_fn, root_dir + out_fn, False, 9, False, False, False, False, True)

def main(csv = "cards.csv"):
    cards = read_csv(csv, sep=",")
    
    for ii, card in enumerate(cards):
        make(title_text = card['Title'],
             card_level = int(card['Level']),
             art_asset_fn = 'assets/' + card['Art'],
             out_fn = 'card_' + str(ii) + '.png')

if __name__ == '__main__':
    main(b'/home/lynn/proj/apocalypse_sirens/small_example/cards.csv')
