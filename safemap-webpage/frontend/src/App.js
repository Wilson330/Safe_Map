import {
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  SliderMark,
  Box,
  Tooltip,
  Button,
  ButtonGroup,
  Flex,
  HStack,
  IconButton,
  Input,
  SkeletonText,
  //Image,
  Text,
} from '@chakra-ui/react'
import { FaLocationArrow, FaTimes } from 'react-icons/fa'
import {
  useJsApiLoader,
  GoogleMap,
  Marker,
  Autocomplete,
  DirectionsRenderer,
} from '@react-google-maps/api'

import { useRef, useState ,useEffect } from 'react'


const center = {lat: 24.795048, lng: 120.9961595}

function App() {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries: ['places'],
  })

  const [map, setMap] = useState(/** @type google.maps.Map */ (null))
  const [directionsResponse, setDirectionsResponse] = useState(null)
  const [distance, setDistance] = useState('')
  useEffect(()=>{
    console.log('wow')
  },[distance])
  const [duration, setDuration] = useState('')
  const [showTooltip, setShowTooltip] = useState(false)
  const [sliderValue, setSliderValue] = useState(50)
  const [routes, setRoutes] = useState([])
  const [markers, setMarkers] = useState([])
  /** @type React.MutableRefObject<HTMLInputElement> */
  const originRef = useRef()
  /** @type React.MutableRefObject<HTMLInputElement> */
  const destinationRef = useRef()
/** @type React.MutableRefObject<HTMLInputElement> */ 
  const weights = useRef()
/** @type React.MutableRefObject<HTMLInputElement> */


  if (!isLoaded) {
    return <SkeletonText />
  }
  async function codeAddress(address) {
    var loc=[];
    // eslint-disable-next-line no-undef
    var geocoder = new google.maps.Geocoder();
    await geocoder.geocode( { 'address': address}, function(results, status) {
      // eslint-disable-next-line no-undef
      if (status === google.maps.GeocoderStatus.OK) {
        loc[0]=results[0].geometry.location.lat();
        loc[1]=results[0].geometry.location.lng();
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
    return loc
  }
  
  function distance2str(distance){
    let m = distance%1000
    if(distance<1000){
      return `${m}m`
    }
    let km = Math.round(distance/10)/100
    return `${km}km`
  }
  function addMarker(position, label) {
    const marker = new window.google.maps.Marker({
      map:map,
      label:{text:label,color:'white'},
      position:position
    });
    markers.push(marker);
  }
  function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    }
    setMarkers([]);
  }
  function addRoute(path,color) {
    const route = new window.google.maps.Polyline({
      map:map,
      path: path,
      geodesic: true,
      strokeColor: color,
      strokeOpacity: 0.8,
      strokeWeight: 5,
    });
    routes.push(route)
  }
  function clearRoute() {
    // setDirectionsResponse(null)
    for (let i = 0; i < routes.length; i++) {
      routes[i].setMap(null);
    }
    setRoutes([]);
  }
  function clearAll(){
    clearRoute()
    clearMarkers()
    setDistance('')
    setDuration('')
    return
  } 
  
  // let markers = [];
  // let routes = [];
  function onCalculateRouteButton(){
    calculateRoute()
  }
  async function calculateRoute() {
    if (originRef.current.value === '' || destinationRef.current.value === '') {
      alert("Please enter origin & destination!!")
      return
    }

    var loc_origin;
    var loc_destination;
    loc_origin = await codeAddress(originRef.current.value);
    loc_destination = await codeAddress(destinationRef.current.value);
    var org = {lat:loc_origin[0],lng:loc_origin[1]}
    var dst = {lat:loc_destination[0],lng:loc_destination[1]}
    // var waypoints_list = [];
    const response = await fetch(`/data?origin=${String(loc_origin)}&destination=${loc_destination}&weights=${sliderValue}`);
    const result = await response.json();
    //const lats = result.lats;
    //const lngs = result.lngs;
    const latlng = result.latlng;

    console.log("latatitude, longtitude", latlng)
    // eslint-disable-next-line no-undef
    var path = latlng.map(x=>({lat:x[0],lng:x[1]}));
    path.splice(0,0,org);
    path.push(dst);

    
    addRoute(path ,"#33AAEE");
    addMarker(org,"A");
    addMarker(dst,"B");
    setDistance(distance2str(result.distance))
    setDuration(`${result.duration}s`)

    // var waypoints_list = latlng.map(x=>({location:new window.google.maps.LatLng(x[0],x[1]),stopover: false}))
    // // eslint-disable-next-line no-undef
    // const directionsService = new google.maps.DirectionsService()
    // const results = await directionsService.route({
	  //   // origin: {lat: 24.797308, lng: 120.995583},
	  //   origin: originRef.current.value,
    //   destination: destinationRef.current.value,
    //   waypoints: waypoints_list,
    //   // eslint-disable-next-line no-undef
    //   //travelMode: google.maps.TravelMode.WALKING,
	  //   travelMode: window.google.maps.TravelMode.BICYCLING
    // })
    // setDirectionsResponse(results)
    
    // setDistance(results.routes[0].legs[0].distance.text)
    // setDuration(results.routes[0].legs[0].duration.text)
  }

  return (
    <Flex
      position='relative'
      flexDirection='column'
      alignItems='center'
      h='100vh'
      w='100vw'
    >
      <Box position='absolute' left={0} top={0} h='100%' w='100%'>
        {/* Google Map Box */}
        <GoogleMap
          center={center}
          zoom={15}
          mapContainerStyle={{ width: '100%', height: '100%' }}
          options={{
            zoomControl: false,
            streetViewControl: false,
            mapTypeControl: false,
            fullscreenControl: false,
          }}
          onLoad={map => setMap(map)}
        >
          <Marker position={center} />
          {directionsResponse && (
            <DirectionsRenderer directions={directionsResponse} />
          )}
        </GoogleMap>
      </Box>
      <Box
        p={4}
        // borderRadius='lg'
        width = "80%"
        m={4}
        bgColor='white'
        shadow='base'
        minW='400px'
        zIndex='1'
      >
        <HStack spacing={2} justifyContent='space-between'>
          <Box width = "30%" minW="50px">
            <Autocomplete>
              <Input type='text' placeholder='Origin' ref={originRef} />
            </Autocomplete>
          </Box>
          <Box width = "30%" minW="50px">
            <Autocomplete>
              <Input
                type='text'
                placeholder='Destination'
                ref={destinationRef}
              />
            </Autocomplete>
          </Box>
          
          <Box width = "25%">
            <Slider 
            aria-label='slider-ex-1' 
            onChange={(val) => setSliderValue(val)}       
            onMouseEnter={() => setShowTooltip(true)}
            onMouseLeave={() => setShowTooltip(false)}
            >
            <SliderMark value={50} mt='1' ml='-2.5' fontSize='sm'>Safety factor</SliderMark>
              <SliderTrack>
                <SliderFilledTrack />
              </SliderTrack>
              <Tooltip
                hasArrow
                bg='#42a6ed'
                color='white'
                placement='top'
                isOpen={showTooltip}
                label={`${sliderValue}%`}
              >
                <SliderThumb />
              </Tooltip>
            </Slider>
          </Box>

          <ButtonGroup>
            <Button colorScheme='pink' type='submit' onClick={onCalculateRouteButton}>
              Calculate Route
            </Button>
            <IconButton
              aria-label='center back'
              icon={<FaTimes />}
              onClick={clearAll}
            />
          </ButtonGroup>
        </HStack>
        <HStack spacing={4} mt={4} justifyContent='space-between'>
          <Text>Distance: {distance} </Text>
          <Text>Duration: {duration} </Text>
          <IconButton
            aria-label='center back'
            icon={<FaLocationArrow />}
            isRound
            onClick={() => {
              map.panTo(center)
              map.setZoom(15)
            }}
          />
        </HStack>
      </Box>
    </Flex>
  )
}

export default App
