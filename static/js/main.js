window.addEventListener('load', () => {
    let selectedDesign = 'mixed_designs';
    let selectedDirection = 'mixed_directions';
  
    function setBackgroundImage() {
      const now = Date.now();
      const width = window.innerWidth;
      const height = window.innerHeight;
      const designParam = `&design=${selectedDesign}`;
      const directionParam = `&direction=${selectedDirection}`;
      const cacheBust = `&cb=${now}`;
      const image = new Image();
      image.onload = () => {
        document.body.style.backgroundImage = `url(${image.src})`;
        document.body.style.backgroundRepeat = 'no-repeat';
        document.body.style.backgroundPosition = 'center';
        document.getElementById('preloader').style.display = 'none';
      };
      image.src = `/bitmap?width=${width}&height=${height}${designParam}${directionParam}${cacheBust}`;
    }
  
    window.onresize = setBackgroundImage;
  
    document.querySelectorAll('.dropdown-item').forEach(item => {
      item.addEventListener('click', e => {
        e.preventDefault();
        if (['mixed_designs','more_lines','more_arcs','only_lines','only_arcs'].includes(item.id)) {
          selectedDesign = item.id;
          dropdownDesignButton.textContent = item.textContent;
        } else {
          selectedDirection = item.id;
          dropdownDirectionButton.textContent = item.textContent;
        }
        setBackgroundImage();
      });
    });
  
    document.getElementById('redrawButton').addEventListener('click', () => {
      setBackgroundImage();
    });
  
    setBackgroundImage();
  });