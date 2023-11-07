
import { Center, Heading, VStack, Text, HStack, Button, SimpleGrid, Image} from "@chakra-ui/react" ;
import { ChakraProvider } from "@chakra-ui/react";
import { useEffect, useState} from "react"


export default function App(){
  const [allPhotos, setAllPhotos] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);


  const onInputChange = e => {

  }
  useEffect(() => {
    fetch("http://127.0.0.1:8000/photos")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setAllPhotos(data);
      });
  }, []);

  return (
    <ChakraProvider>
    <Center bg="black" color="white" padding={8}>
      <VStack spacing={7}>
        <Heading>
          Funny Animal Pictures
        </Heading>
        <Text>
        Smile every day and look at the photos.
        </Text>
        <HStack>
          <input type="file" onChange={onInputChange} onClick={onFileUpload}></input>
          <Button size= "lg" colorScheme="red" isDisabled={null} onClick={null} Upload Picture ></Button>
        </HStack>

        <Heading>
          Your photos
        </Heading>
        <SimpleGrid columns={3} spacing={8}>
          {allPhotos.map((photo) => {
            return (
              <Image
                borderRadius={25}
                boxSize="300px"
                src={photo["photo_url"]}
                fallbackSrc="https://via.placeholder.com/150"
                objectFit="cover"/>
            );
          })}

        </SimpleGrid>
      </VStack> 

    </Center>
    </ChakraProvider>
  )
}