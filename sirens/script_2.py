def read_line(headers, line, sep='§', replace_with_linebreak='¶'):
    """
    :param headers: List of string, Headers of a CSV
    :param line:    List of 
    :param sep:
    
    :returns: Dict of string --> value
    
    >>> read_line(['width', 'height', 'shape'], '3.0, 2.0, rectangle', 'n')
    {'width' : '3.0', 'height' : '2.0', 'shape' : 'rectangle'}
    """
    
    out = {key : value.strip()
            for key, value in zip(headers, line.strip().split(sep))}
    
    if replace_with_linebreak is not None:
        for key in out.keys():
                out[key] = out[key].replace(replace_with_linebreak, '\n')
    
    return out

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
         power_level    = 1,
         sacr_value     = 6,
         summ_level     = 4,
         muse           = "Tri",
         details        = "(deets)",
         art_asset_fn   = b'assets/master_chief.png',
         out_fn         = b'cards/example_out.png',
         max_title_len  = 1125,
         source_fn      = b'bossfights_trial.xcf',
         root_dir       = b'/home/lynn/proj/apocalypse_sirens/sirens/'):
    
    print("Load image")
    img = pdb.gimp_xcf_load(0, root_dir + source_fn, root_dir + source_fn)
    # 2. Set Title Text
    # img = gimp.image_list()[0]
    # This layer should be named 'Title', and should be set to 'Dynamic'
    
    print("Create title layer")
    title_layer = pdb.gimp_image_get_layer_by_name(img, 'Title')
    if title_text is not None:
        pdb.gimp_text_layer_set_text(title_layer, ' ' + title_text)
        # Resize Title layer if it is long, iteratively squeezing it down
        # (Note: Layer must be set 'dynamic', not fixed)
        curr_width = pdb.gimp_drawable_width(title_layer)
        while curr_width > max_title_len:
            # Make space by shrinking spacing
            if pdb.gimp_text_layer_get_letter_spacing(title_layer) > -5.0:
                pdb.gimp_text_layer_set_letter_spacing(title_layer,
                    pdb.gimp_text_layer_get_letter_spacing(title_layer) - 0.2)
            # Still doesn't work? Reduce text size
            else:
                # 180 is the exact height of the title text
                pdb.gimp_layer_scale(title_layer, max_title_len, 180, False)
                # (171, 180) is the exact coordinate of the top left of the title
                pdb.gimp_layer_set_offsets(title_layer, 171, 180)
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
        pdb.plug_in_gauss_iir(img, title_copy, 12.0, True, True)
        pdb.gimp_drawable_levels(title_copy, 4, 0.0, 0.5, False, 1.0, 0.0, 1.0, False)
    else:
        pdb.gimp_text_layer_set_text(title_layer, ' ')
    
    # 3: Set power level!
    print("Set power level")
    power_layer = pdb.gimp_image_get_layer_by_name(img, 'Power')
    power_glow = pdb.gimp_image_get_layer_by_name(img, 'Power_Glow')
    if power_level is None or power_level == 0:
        pdb.gimp_drawable_set_visible(power_layer, False)
        pdb.gimp_drawable_set_visible(power_layer, False)
    else:
        pdb.gimp_drawable_set_visible(power_layer, True)
        pdb.gimp_drawable_set_visible(power_layer, True)
        pdb.gimp_text_layer_set_text(power_layer, str(power_level))
    
    # 4: Set sacr values!
    print("Set summoning values")
    summ_layers = [pdb.gimp_image_get_layer_by_name(img, 'Eye_' + str(x)) for x in range(1,9)]
    sacr_layers = [pdb.gimp_image_get_layer_by_name(img, 'Skull_' + str(x)) for x in range(1,9)]
    
    # set them invis first
    for level_layer in summ_layers:
        pdb.gimp_item_set_visible(level_layer, False)
    
    for level_layer in sacr_layers:
        pdb.gimp_item_set_visible(level_layer, False)
    
    # then make them visible
    if summ_level is not None and not len(summ_level) == 0: 
        for ii in range(int(summ_level)):
            pdb.gimp_item_set_visible(summ_layers[ii], True)
    
    if sacr_value is not None and not len(sacr_value) == 0:
        for ii in range(int(sacr_value)):
            pdb.gimp_item_set_visible(sacr_layers[ii], True)
    
    # 5. Set layer description
    print("Set description")
    details_text = details.replace('§', '\n')
    detail_layer = pdb.gimp_image_get_layer_by_name(img, 'Details')
    if details is not None:
        pdb.gimp_text_layer_set_text(detail_layer, details_text)
    
    # 5. Set Muse
    print("Muse")
    muse_names = ['Red', 'Green', 'Blue', 'Tri', 'United']
    red_icon    = pdb.gimp_image_get_layer_by_name(img, 'Red_Muse')
    blue_icon   = pdb.gimp_image_get_layer_by_name(img, 'Blue_Muse')
    green_icon  = pdb.gimp_image_get_layer_by_name(img, 'Green_Muse')
    united_icon = pdb.gimp_image_get_layer_by_name(img, 'United_Muse')
    tri_icon    = pdb.gimp_image_get_layer_by_name(img, 'Tri_Muse')
    
    print("... ... Invis muses")
    for layer in [red_icon, blue_icon, green_icon, united_icon, tri_icon]:
        print(layer)
        pdb.gimp_item_set_visible(layer, False)
    
    print("... ... Setting muse up")
    if muse == 'R':
        pdb.gimp_item_set_visible(red_icon, True)
    elif muse == 'G':
        pdb.gimp_item_set_visible(green_icon, True)
    elif muse == 'B':
        pdb.gimp_item_set_visible(blue_icon, True)
    elif muse == 'Tri':
        pdb.gimp_item_set_visible(tri_icon, True)
    elif muse == 'United':
        pdb.gimp_item_set_visible(united_icon, True)
    
        
    # 7. set art
    print("Set art")
    art_layer = pdb.gimp_file_load_layer(img, root_dir + art_asset_fn)
    img.add_layer(art_layer)
    # raise layer above the bottom
    pdb.gimp_image_lower_item_to_bottom(img, art_layer)
    pdb.gimp_image_raise_item(img, art_layer)
    
    # 8. blur art
    print("Blur art")
    blur_mask = detail_layer = pdb.gimp_image_get_layer_by_name(img, 'Blur_Mask')
    select = pdb.gimp_image_select_item(img, 2, blur_mask)
    pdb.plug_in_gauss_iir(img, art_layer, 128.0, True, True)
    
    # 9. Merge layers
    print("Merge layers")
    pdb.gimp_image_merge_visible_layers(img, 1)
    drw = pdb.gimp_image_get_active_drawable(img)
    
    # 10. export
    print("Export")
    pdb.gimp_edit_copy_visible(img)
    full_out_fn = root_dir + out_fn + ".png"
    full_out_fn = full_out_fn.replace(" ","_")
    pdb.file_png_save(img, drw, full_out_fn, full_out_fn, False, 9, False, False, False, False, True)
    
    # 11. delete
    print("Delete")
    pdb.gimp_image_delete(img)


def main(csv = b'/home/lynn/proj/apocalypse_sirens/sirens/spirits.csv',
         start_from = 0):
    cards = read_csv(csv, sep="§")
    
    for ii, card in enumerate(cards[start_from:]):
        print("Making card " + str(ii))
        make(title_text = card['name'],
         power_level    = card['pow'],
         sacr_value     = card['sacr_val'],
         summ_level     = card['sum_cost'],
         muse           = card['muse'],
         details        = card['details'],
         art_asset_fn   = b'assets/' + card['asset'].encode('ascii'),
         out_fn         = b'cards/' + card['name'].encode('ascii'),
         max_title_len  = 1125,
         root_dir       = b'/home/lynn/proj/apocalypse_sirens/sirens/'
        )

    # todo - modify exported filenames to have underscores instead of spaces, and end with .png

