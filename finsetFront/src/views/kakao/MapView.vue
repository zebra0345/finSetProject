<template>
  <div>
    <h1 class="page-title">
      <v-icon start>mdi-map-search-outline</v-icon>
      은행 위치 검색 서비스
    </h1>

    <!-- 시 선택 -->
    <div class="input-group">
      <v-icon start>mdi-city</v-icon>
      <label for="city">시 선택:</label>
      <select v-model="selectedCity" @change="fetchDistricts">
        <option value="">시를 선택하세요</option>
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
      </select>
    </div>

    <!-- 군/구 선택 -->
    <div class="input-group">
      <v-icon start>mdi-map-marker</v-icon>
      <label for="district">군/구 선택:</label>
      <select v-model="selectedDistrict">
        <option value="">군/구를 선택하세요</option>
        <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
      </select>
    </div>

    <!-- 검색어 입력 -->
    <div class="input-group">
      <v-icon start>mdi-magnify</v-icon>
      <label for="keyword">검색어:</label>
      <input v-model="keyword" type="text" placeholder="검색할 장소를 입력하세요" />
    </div>

    <!-- 검색 버튼 -->
    <button class="search-button" @click="searchPlaces">
      <v-icon start>mdi-search-web</v-icon>
      검색하기
    </button>

    <!-- 카카오 맵 -->
    <div id="map" class="map-container"></div>
  </div>
</template>

<script>
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const selectedCity = ref('');
    const selectedDistrict = ref('');
    const keyword = ref('');
    const cities = ref([
      '서울특별시',
      '부산광역시',
      '대구광역시',
      '인천광역시',
      '광주광역시',
      '대전광역시',
      '울산광역시',
      '세종특별자치시',
      '경기도',
      '강원도',
      '충청북도',
      '충청남도',
      '전라북도',
      '전라남도',
      '경상북도',
      '경상남도',
      '제주특별자치도',
    ]);
    const districts = ref([]);
    let map = null;
    let markers = [];

    const initMap = () => {
      if (window.kakao && window.kakao.maps) {
        const mapContainer = document.getElementById('map');
        const mapOption = {
          center: new kakao.maps.LatLng(37.5665, 126.9780),
          level: 5,
        };
        map = new kakao.maps.Map(mapContainer, mapOption);
      } else {
        console.error('카카오맵 API 로드 실패');
      }
    };

    const fetchDistricts = () => {
      const districtData = {
        '서울특별시': ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구'],
        '부산광역시': ["중구",
        "서구",
        "동구",
        "영도구",
        "부산진구",
        "동래구",
        "남구",
        "북구",
        "해운대구",
        "사하구",
        "금정구",
        "강서구",
        "연제구",
        "수영구",
        "사상구",
        "기장군",],
        '대구광역시': ["중구",
        "동구",
        "서구",
        "남구",
        "북구",
        "수성구",
        "달서구",
        "달성군",
        "군위군",],
        '인천광역시': ["중구",
        "동구",
        "미추홀구",
        "연수구",
        "남동구",
        "부평구",
        "계양구",
        "서구",
        "강화군",
        "옹진군",],
        '광주광역시': ['서구', '남구', '북구', '동구', '광산구'],
        '대전광역시': ['동구', '중구', '서구', '유성구', '대덕구'],
        '울산광역시': ['남구', '중구', '동구', '북구', '울주군'],
        '세종특별자치시': ['조치원읍', '연기면'],
        '경기도': ["수원시",
        "고양시",
        "용인시",
        "성남시",
        "부천시",
        "화성시",
        "안산시",
        "남양주시",
        "안양시",
        "평택시",
        "시흥시",
        "파주시",
        "의정부시",
        "김포시",
        "광주시",
        "광명시",
        "군포시",
        "하남시",
        "오산시",
        "양주시",
        "이천시",
        "구리시",
        "안성시",
        "포천시",
        "의왕시",
        "양평군",
        "여주시",
        "동두천시",
        "가평군",
        "과천시",
        "연천군",],
        '강원도': ["춘천시",
        "원주시",
        "강릉시",
        "동해시",
        "태백시",
        "속초시",
        "삼척시",
        "홍천군",
        "횡성군",
        "영월군",
        "평창군",
        "정선군",
        "철원군",
        "화천군",
        "양구군",
        "인제군",
        "고성군",
        "양양군",],
        '충청북도': ["청주시",
        "충주시",
        "제천시",
        "보은군",
        "옥천군",
        "영동군",
        "증평군",
        "진천군",
        "괴산군",
        "음성군",
        "단양군",],
        '충청남도': ["천안시",
        "공주시",
        "보령시",
        "아산시",
        "서산시",
        "논산시",
        "계룡시",
        "당진시",
        "금산군",
        "부여군",
        "서천군",
        "청양군",
        "홍성군",
        "예산군",
        "태안군",],
        '전라북도': ['전주시', '군산시', '익산시'],
        '전라남도': ["목포시",
        "여수시",
        "순천시",
        "나주시",
        "광양시",
        "담양군",
        "곡성군",
        "구례군",
        "고흥군",
        "보성군",
        "화순군",
        "장흥군",
        "강진군",
        "해남군",
        "영암군",
        "무안군",
        "함평군",
        "영광군",
        "장성군",
        "완도군",
        "진도군",
        "신안군",],
        '경상북도': ["포항시",
        "경주시",
        "김천시",
        "안동시",
        "구미시",
        "영주시",
        "영천시",
        "상주시",
        "문경시",
        "경산시",
        "의성군",
        "청송군",
        "영양군",
        "영덕군",
        "청도군",
        "고령군",
        "성주군",
        "칠곡군",
        "예천군",
        "봉화군",
        "울진군",
        "울릉군",],
        '경상남도': ["창원시",
        "진주시",
        "통영시",
        "사천시",
        "김해시",
        "밀양시",
        "거제시",
        "양산시",
        "의령군",
        "함안군",
        "창녕군",
        "고성군",
        "남해군",
        "하동군",
        "산청군",
        "함양군",
        "거창군",
        "합천군",],
        '제주특별자치도': ['제주시', '서귀포시'],
    

      };

      districts.value = districtData[selectedCity.value] || [];
      selectedDistrict.value = '';
    };

    const searchPlaces = () => {
      if (!selectedCity.value || !selectedDistrict.value || !keyword.value) {
        alert('시, 군/구, 그리고 검색어를 입력해주세요.');
        return;
      }

      const searchParams = {
        city: selectedCity.value,
        district: selectedDistrict.value,
        keyword: keyword.value,
      };

      axios
        .post('http://127.0.0.1:8000/kakao/serchMap/', searchParams)
        .then((response) => {
          const places = response.data.places;

          removeMarkers();
          places.forEach((place) => {
            const position = new kakao.maps.LatLng(place.lat, place.lon);
            const marker = new kakao.maps.Marker({
              position: position,
              map: map,
            });

            const infoWindow = new kakao.maps.InfoWindow({
              content: `<div style="padding:5px;">${place.name}</div>`,
            });

            kakao.maps.event.addListener(marker, 'mouseover', () => {
              infoWindow.open(map, marker);
            });

            kakao.maps.event.addListener(marker, 'mouseout', () => {
              infoWindow.close();
            });

            markers.push(marker);
          });

          if (places.length > 0) {
            const moveLatLon = new kakao.maps.LatLng(places[0].lat, places[0].lon);
            map.setCenter(moveLatLon);
          }
        })
        .catch((error) => {
          console.error('Error fetching places:', error);
        });
    };

    const removeMarkers = () => {
      markers.forEach((marker) => {
        marker.setMap(null);
      });
      markers = [];
    };

    watch(selectedCity, fetchDistricts);

    onMounted(() => {
      initMap();
    });

    return {
      selectedCity,
      selectedDistrict,
      keyword,
      cities,
      districts,
      searchPlaces,
    };
  },
};
</script>

<style scoped>
.page-title {
  font-size: 1.5em;
  font-weight: bold;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

input,
select {
  flex: 1;
  margin-left: 10px;
  padding: 5px;
}

.search-button {
  display: flex;
  align-items: center;
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  border-radius: 4px;
}

.search-button v-icon {
  margin-right: 5px;
}

.map-container {
  width: 100%;
  height: 350px;
  margin-top: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
