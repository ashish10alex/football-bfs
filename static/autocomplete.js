// Autocomplete code inspired from - https://www.w3schools.com/howto/howto_js_autocomplete.asp
// Modification from the example in the link includes - Use of fuzzy search library Fuse
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/

      results = fuse.search(e.target.value)
      for (i=0; i < 6; i++){
            b = document.createElement("DIV")
            b.innerHTML += results[i].item
            b.innerHTML += "<input type='hidden' value='" + results[i].item + "'>";
            a.appendChild(b);
           b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          }); 
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}


// an array containing name of players - used for fuzzy autocomplete
var players = [
    'Rogério Ceni',
     'M. Riemann',
     'M. Neuer',
     'J. Pickford',
     'P. Gazzaniga',
     'E. Martínez',
     'M. Maignan',
     'A. Onana',
     'L. Messi',
     'Ederson',
     'De Gea',
     'M. ter Stegen',
     'L. Hoyos',
     'R. Ofori',
     'N. Guzmán',
     'J. Oblak',
     'E. Unsain',
     'Alisson',
     'F. Muslera',
     'G. Donnarumma',
     'S. Ortega',
     'Guaita',
     'A. Lopes',
     'H. Lloris',
     'A. Marchesín',
     'B. Leno',
     'Nelsildo Reis',
     'Rui Patrício',
     'K. Schmeichel',
     '14\xa0Fábio',
     '14\xa0M. Landreau',
     'J. Omlin',
     'Y. Sommer',
     'J. Hansen',
     'Pau López',
     'Aitor',
     'J. Drommel',
     'A. Talavera',
     'M. Borjan',
     'L. Burián',
     'D. Livaković',
     '14\xa0Pinto',
     'J. Bursik',
     'Adán',
     'C. Lucchetti',
     'T. Courtois',
     'Andrés Fernández',
     'U. Çakır',
     'G. Herrera',
     'T. Vaclík',
     'A. Federici',
     'Pepe Reina',
     'W. Szczęsny',
     'Kiko Casilla',
     '14\xa0Cássio',
     'G. Rulli',
     'K. Casteels',
     'Juan Carlos',
     'L. Mejía',
     'V. Milinković-Savić',
     'V. Stojković',
     'Diego Mariño',
     'Pacheco',
     'G. Arias',
     'A. McGregor',
     'P. Gulácsi',
     'David Raya',
     'D. von Ballmoos',
     'A. Rossi',
     'Cantero',
     'M. Pigliacelli',
     'J. Zoet',
     'S. Sosa',
     'Álex Remiro',
     'S. Nishikawa',
     'S. Handanovič',
     'S. Mignolet',
     'G. Castellón',
     'G. Güvenç',
     'W. Benítez',
     'E. Andrada',
     'Unai Simón',
     'C. Vargas',
     '21\xa0M. Fraga',
     'H. Van Crombrugge',
     'N. Pope',
     'P. Pentz',
     'M. Campaña',
     'David Soria',
     'M. Schuhen',
     'W. Hahn',
     '11\xa0E. van der Sar',
     'P. Carlgren',
     'Munir',
     'Roberto',
     'E. Room',
     'Lucas Mantela',
     'G. Buffon',
     'O. Baumann',
     'J. Alnwick',
     'S. Viera',
     'J. Huth',
     'L. Fabiański',
     'A. Hansen',
     'O. Vlachodimos',
     'Dani Jiménez',
     'J. Siebenhandl',
     '20\xa0J. Herrera',
     'G. Ochoa',
     'M. Crépeau',
     'S. Scuffet',
     'M. Bizot',
     'D. Subašić',
     'Y. Bounou',
     'J. Lewis',
     'V. Hladký',
     'B. Peacock-Farrell',
     'J. Rinne',
     'A. McCarthy',
     'L. García',
     'T. Krul',
     'S. Johnstone',
     'Yan Junling',
     '21\xa0A. Lindegaard',
     'I. Akinfeev',
     '21\xa0K. Westwood',
     'S. Sirigu',
     '21\xa0M. El Shenawy',
     'Matheus',
     'A. Gomis',
     '21\xa0Denis',
     'D. Bouzanis',
     'S. Bolat',
     'L. Acosta',
     'K. Trapp',
     'T. Melia',
     'S. Johnson',
     'M. Silvestri',
     'P. Jensen',
     'Manolo Reina',
     'P. Gallese',
     'S. Rossbach',
     'A. Lafont',
     'W. Yarbrough',
     'Robert Sanchéz',
     '17\xa0Victor Valdés',
     'J. Bijlow',
     'M. Sels',
     'Herrerín',
     '21\xa0Gu Chao',
     'B. Drągowski',
     'S. Dioudis',
     'A. Al Mayoof',
     'A. Oukidja',
     'José Sá',
     'J. Hart',
     'A. Aguilar',
     'Bracali',
     'S. Kritsyuk',
     'A. Cragno',
     'T. Kaminski',
     'Simão Donatinho',
     'D. Bentley',
     'Riesgo',
     'K. Nordfeldt',
     'J. Musso',
     'C. MacGillivray',
     'P. Kieszek',
     'Fernando',
     'H. González',
     'A. Aguerre',
     '20\xa0T. Howard',
     'J. Blaswich',
     'M. Gersbeck',
     'R. Rey',
     'J. Butez',
     'Guilherme',
     '21\xa0R. Williams',
     '21\xa0Beto',
     'A. Pyatov',
     '21\xa0J. Serendero',
     '20\xa0A. Kwarasey',
     'T. Horn',
     'M. Männel',
     'T. Carson',
     'Rui Silva',
     'A. Shunin',
     'R. Zentner',
     'A. Consigli',
     'D. Bachmann',
     'S. Lung',
     'D. Azcona',
     'R. Boffin',
     'J. Bond',
     'V. Babacan',
     'Samuel Portugal',
     'K. Lamprou',
     '16\xa0Weverton',
     'J. Ledesma',
     'M. Dituro',
     'B. Samba',
     'A. Paschalakis',
     'S. Gonda',
     'E. Mulder',
     'Raphaelinho Anjos',
     'Diego López',
     'J. Leca',
     'A. Montero',
     'S. Dimitrievski',
     'L. Southwood',
     'S. Sluga',
     'S. Rochet',
     'L. Hrádecký',
     '16\xa0Victor',
     '08\xa0O. Kahn',
     'H. Koffi',
     'D. Léon',
     'P. Kühn',
     'O. Kolář',
     'M. Díaz',
     'S. Marinović',
     'A. Nübel',
     'D. Ospina',
     'D. Mitov',
     'W. Aguerre',
     'N. Haikin',
     'C. Bonilla',
     'J. Corona',
     'I. Meslier',
     'R. Olsen',
     'Gabri Prestão',
     'A. Blake',
     'C. Álvarez',
     '21\xa0Cássio',
     'B. Reynet',
     'B. Costil',
     'M. Diaw',
     'Germán Parreño',
     'E. Audero',
     'B. Hamid',
     'R. Gudiño',
     'E. Viviano',
     'M. Andújar',
     'J. Leutwiler',
     'T. Didillon',
     'R. Riou',
     'B. Guzan',
     'G. Lajud',
     'J. Espínola',
     'J. Brinkies',
     'G. Gallon',
     'M. Al Owais',
     'Gabriel',
     'G. Akkan',
     'N. Marsman',
     'Pierrino Faria',
     'T. Wellenreuther',
     'Óscar Whalley',
     'F. Altamirano',
     'K. Dawson',
     'S. George',
     'F. Müller',
     'N. Vikonis',
     'Marcelo Grohe',
     'C. Gordon',
     '20\xa0J. Gonzalez',
     'M. Maroši',
     'A. Bono',
     'L. Thomas',
     'M. Turner',
     'M. Stekelenburg',
     'C. Dawson',
     'L. Zigi',
     'F. Kaplan',
     'L. Skorupski',
     'B. Hamer',
     'V. Demarconnay',
     'Jo Hyeon Woo',
     'E. Mendy',
     'R. Zieler',
     'Luís Maximiano',
     'Kim Seung Gyu',
     'Y. Brecher',
     "R. O'Donnell",
     'Kang Hyeon Mu',
     'Raúl Lizoain',
     'Raúl Fernández',
     'Y. van Osch',
     'O. Sail',
     '21\xa0L. Camp',
     'B. Jones',
     'P. Tytoń',
     'L. Montipò',
     'M. Barovero',
     '21\xa0D. Bingham',
     'T. Königsmann',
     'P. Bråtveit',
     'J. Dahlin',
     'Juan Soriano',
     'G. Morris',
     'P. Leeuwenburgh',
     'André Moreira',
     'B. Białkowski',
     'A. Silva',
     'F. Woodman',
     'M. van der Hart',
     'S. Torrico',
     'G. Kobel',
     'S. Cleveland',
     'Victorino Magela',
     'C. Stanković',
     '19\xa0Fabiano',
     'R. Gikiewicz',
     'P. Bernardoni',
     'P. Abrahamsson',
     'M. Müller',
     'K. Roos',
     'D. Phillips',
     'M. Flekken',
     'N. Larsen',
     'J. Talbot',
     'A. Schwolow',
     'M. Kolke',
     'C. Mathenia',
     'S. Moore',
     '21\xa0J. McKeown',
     'J. Lössl',
     'J. Maurer',
     'J. Lumley',
     'B. Collins',
     'P. Nardi',
     'J. Day',
     'S. Kırıntılı',
     'D. Stockdale',
     'A. Linde',
     'V. Jaroš',
     'A. Luthe',
     'K. Müller',
     'H. Lindner',
     'L. Kelly',
     'M. Sandberg',
     '19\xa0E. Galekovic',
     'D. Stipica',
     'Yang Han Been',
     'K. Haug',
     '20\xa0M. Agazzi',
     'S. McDermott',
     'O. Jansson',
     'B. Amos',
     'Fred Aníbão',
     'C. Maxwell',
     'C. Rigamonti',
     'D. Iversen',
     'M. Zetterer',
     'D. Odumosu',
     'A. Mannus',
     'R. Fährmann',
     'A. Maraval',
     'D. Heuer Fernandes',
     'E. Basilio',
     '20\xa0A. Collin',
     'B. Stuver',
     'L. Roberts',
     'Z. Clark',
     'A. Olliero',
     'E. Taşkıran',
     'Kaíquão Castro',
     'V. Belec',
     '21\xa0R. Pleșca',
     'Yang Hyung Mo',
     'M. Marić',
     'M. Silva',
     'M. Schubert',
     'E. McGinty',
     'F. Al Qarni',
     'M. Ibáñez',
     'A. Kofler',
     'A. Singh',
     'G. Hubert',
     'S. Burchert',
     'K. Grabara',
     'R. Gurtner',
     'R. Romo',
     'D. Ousted',
     'J. Carvallo',
     'S. Dieng',
     'J. Staněk',
     'M. Dupé',
     '21\xa0N. Jackers',
     'Charles',
     '21\xa0S. Gbohouo',
     'P. Farman',
     'P. Sprint',
     'G. Singh Sandhu',
     'J. Stevens',
     'I. Gelios',
     'M. Koval',
     'K. Eissa',
     'L. Unnerstall',
     'T. Vincensini',
     'D. Batz',
     'M. Travers',
     'M. Hermansen',
     'Kim Jin Hyeon',
     'R. Strebinger',
     'F. Plach',
     'M. Vanhamel',
     '21\xa0G. Chatterjee',
     'M. Macey',
     'L. Nicholls',
     'M. Branderhorst',
     'N. Gartside',
     'Jean',
     'E. Domaschke',
     '21\xa0M. Howard',
     '20\xa0G. Banguera',
     '18\xa0S. Elana',
     'M. Okoye',
     'F. Niță',
     'L. Vigouroux',
     'A. Legzdins',
     'M. Stryjek',
     'Jung Sung Ryong',
     '20\xa0N. Leali',
     'A. Abedzadeh',
     'L. Unbehaun',
     'T. Rönning',
     'M. Zeghba',
     'P. Drewes',
     'W. Jääskeläinen',
     'Z. Alomerović',
     'T. King',
     'N. Mäenpää',
     'M. Vandevoordt',
     'M. Langerak',
     'Park Il Gyu',
     'J. Marcinkowski',
     'T. Miller',
     'J. Coleman',
     'R. Lainton',
     'S. Flinders',
     'M. Higashiguchi',
     'J. Graterol',
     'Miguel Silva',
     'A. Østbø',
     'M. Di Gregorio',
     '17\xa0M. Sifakis',
     '21\xa0C. Doyle',
     'S. Şahin-Radlinger',
     'S. Brodersen',
     'D. Cornell',
     'N. Baumann',
     'A. Maksimenko',
     'Carlos Miguel',
     'S. Rojas',
     '08\xa0M. Ballotta',
     'N. Thiede',
     'B. Leroy',
     'L. McGee',
     'J. Andrésson',
     'G. Mamardashvili',
     'D. Reimann',
     'L. Johansson',
     'J. Wollacott',
     'B. Allain',
     'V. Kovacević',
     'A. Bodart',
     'C. Rushworth',
     'I. Eğribayat',
     'A. Desmas',
     'B. Murphy',
     'N. Trott',
     'M. Ingram',
     'P. Rajković',
     'P. Ortíz',
     'M. Ilic',
     'Y. Oki',
     'A. Bayındır',
     'C. Cáceda',
     '21\xa0G. Athanasiadis',
     'M. Paes',
     'N. Tzanev',
     'I. Grbić',
     'A. Paleari',
     'S. Lukić',
     'G. Bushchan',
     'A. Fisher',
     'R. Bentancur',
     'K. Tani',
     'N. Lemaître',
     '21\xa0L. Raeder',
     'A. Keita',
     'Daniel Figueira',
     'Z. Frelih',
     'J. Griffiths',
     'J. Dixon',
     'M. Prévot',
     '21\xa0B. Büchel',
     'E. Green',
     'G. Vicario',
     'W. Ramírez',
     'P. Köhn',
     'M. Nicolas',
     'A. Cairns',
     'F. Kastenmeier',
     'Song Bum Keun',
     'H. Iikura',
     'L. Grill',
     'S. Roy',
     'P. Dahlberg',
     'F. Majchrowicz',
     'M. Aioani',
     'A. Whiteman',
     'Y. Takaoka',
     'C. Eriksson',
     'A. Meyer',
     'D. Dibusz',
     'M. Hiller',
     'G. Bazunu',
     'L. Chevalier',
     'D. Akpeyi',
     'M. Eșanu',
     'J. Fejzić',
     'J. Cumming',
     'Mateus Pasinato',
     'T. Glover',
     'H. Bonmann',
     'D. Schmidt',
     'M. Cooper',
     '21\xa0J. Moreno',
     'O. Kocuk',
     'Lucas Covolan',
     'M. Nawaz',
     'Y. Fofana',
     'Joan Femenías',
     'M. Šarkić',
     'M. Lukov',
     'L. Malagón',
     'J. Pantemis',
     'T. Romero',
     'E. Dos Santos Haesler',
     'D. Ochoa',
     'N. Bishop',
     'E. Destanoğlu',
     'J. Anang',
     'M. Christiansen',
     'G. Hatano',
     'F. Buntić',
     'K. Broll',
     'Altube',
     'T. Schreiber',
     'M. Trmal',
     'R. Hoffmann',
     'B. Niasse',
     'Ayesa',
     'M. Lis',
     'V. Johansson',
     'Luiz Júnior',
     'P. Menzel',
     'D. Singh Moirangthem',
     'T. Casali',
     'Q. Braat',
     '21\xa0P. Gavilán',
     'C. Miszta',
     'L. Weinkauf',
     'A. Nurudeen',
     'F. Stritzel',
     'G. Dietsch',
     'Choi Young Eun',
     'N. Sauter',
     'J. Zetterström',
     'V. Kaith',
     'J. Trafford'
]

const fuse = new Fuse(players)
autocomplete(document.getElementById("PlayerOne"), players);
autocomplete(document.getElementById("PlayerTwo"), players);
