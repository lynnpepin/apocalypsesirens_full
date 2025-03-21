title_text     = 'DOCTOR TOOTS 300000'
power_level    = 1
sacr_value     = 6
summ_level     = 4
details = "(We were slaves to the very memes that we had created. We toiled to earn the privilege of being distracted by them.)§§Oh... Dirk..." # They fiddled while Rome burned, and we threw ourselves into the fire so that we might listen to the music. The memes had us. Or, rather, they could has us.
art_asset_fn   = b'assets/master_chief.png'
out_fn         = b'cards/example_out.png'
max_title_len  = 1125
root_dir       = b'/home/lynn/proj/apocalypse_sirens/sirens/'

#img = pdb.gimp_xcf_load(0, root_dir + source_fn, root_dir + source_fn)
img = gimp.image_list()[0]

# 2. Set Title Text
# img = gimp.image_list()[0]
# This layer should be named 'Title', and should be set to 'Dynamic'
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
summ_layers = [pdb.gimp_image_get_layer_by_name(img, 'Eye_' + str(x)) for x in range(1,9)]
sacr_layers = [pdb.gimp_image_get_layer_by_name(img, 'Skull_' + str(x)) for x in range(1,9)]

# set them invis first
for level_layer in summ_layers:
    pdb.gimp_item_set_visible(level_layer, False)

for level_layer in sacr_layers:
    pdb.gimp_item_set_visible(level_layer, False)

# then make them visible
if summ_level is not None and summ_level > 0:
    for ii in range(int(summ_level)):
        pdb.gimp_item_set_visible(summ_layers[ii], True)

if sacr_value is not None and sacr_value > 0:
    for ii in range(int(sacr_value)):
        pdb.gimp_item_set_visible(sacr_layers[ii], True)

# 5. Set layer description
details_text = details.replace('§', '\n')
detail_layer = pdb.gimp_image_get_layer_by_name(img, 'Details')
if details is not None:
    pdb.gimp_text_layer_set_text(detail_layer, details_text)


# 6. set art
art_layer = pdb.gimp_file_load_layer(img, root_dir + art_asset_fn)
img.add_layer(art_layer)
# raise layer above the bottom
pdb.gimp_image_lower_item_to_bottom(img, art_layer)
pdb.gimp_image_raise_item(img, art_layer)


# 7. blur art
blur_mask = detail_layer = pdb.gimp_image_get_layer_by_name(img, 'Blur_Mask')
select = pdb.gimp_image_select_item(img, 2, blur_mask)
pdb.plug_in_gauss_iir(img, art_layer, 128.0, True, True)


# 8. Merge layers
pdb.gimp_image_merge_visible_layers(img, 1)
drw = pdb.gimp_image_get_active_drawable(img)

# 9. export
pdb.gimp_edit_copy_visible(img)
pdb.file_png_save(img, drw, root_dir + out_fn, root_dir + out_fn, False, 9, False, False, False, False, True)


