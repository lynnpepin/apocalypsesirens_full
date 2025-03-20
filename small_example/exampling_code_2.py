"""
These are just notes about interacting with an image through Gimp-Fu!

Parts to finish here:
1. Do over all CSVs
2. Optional export to xcf
3. Info box
"""

def main(title_text     = 'DOCTOR TOOTS 300000',
         card_level     = 3,
         art_asset_fn   = b'assets/art_1.png',
         out_fn         = b'out_1.png',
         max_title_len  = 200,
         source_fn      = b'example.xcf',
         root_dir       = b'/home/lynn/proj/apocalypse_sirens/'):
         
    # Load xcf
    img = pdb.gimp_xcf_load(0, root_dir + source_fn, root_dir + source_fn)
    
    # Set Title Text
    #img = gimp.image_list()[0]
    # text layer should be dynamic...
    title_layer = pdb.gimp_image_get_layer_by_name(img, 'Title')
    pdb.gimp_text_layer_set_text(title_layer, title_text)
    
    ## Resize Title if too long
    ## (Note: Layer must be set 'dynamic', not fixed)
    curr_width = pdb.gimp_drawable_width(title_layer)
    
    while curr_width > max_title_len:
        pdb.gimp_text_layer_set_letter_spacing(title_layer,
            pdb.gimp_text_layer_get_letter_spacing(title_layer) - 0.2)
        
        curr_width = pdb.gimp_drawable_width(title_layer)
        # Consider: Don't let spacing get < some size;
        # once spacing hits -4.0, start reducing font size or something?
    
    
    ## Title shadow
    title_copy = title_layer.copy(False)
    pdb.gimp_image_set_active_layer(img, title_layer)
    img.add_layer(title_copy)
    pdb.gimp_image_lower_layer(img, title_copy)
    pdb.gimp_layer_resize_to_image_size(title_copy)
    pdb.gimp_drawable_invert(title_copy, 1)
    pdb.plug_in_gauss_iir(img, title_copy, 6.0, 4, 4)
    pdb.gimp_drawable_levels(title_copy, 4, 0.0, 0.5, False, 1.0, 0.0, 1.0, False)
    
    # Set levels
    level_layers = [pdb.gimp_image_get_layer_by_name(img, 'Level_' + str(x)) for x in [1, 2, 3, 4]]
    for level_layer in level_layers:
        pdb.gimp_item_set_visible(level_layer, False)
    
    for ii in range(card_level):
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
