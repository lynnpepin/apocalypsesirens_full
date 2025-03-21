for file in cards/*.png; do
  filename=$(basename -- "$file");
  extension=${filename##*.}"
  filename="${filename%.*}"
  convert "cards/$filename.$extension" "cards_jpg/$filename.jpg"
done

