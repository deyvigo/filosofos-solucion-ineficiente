import ImageMesa from './assets/filosofoschinos.png'
import { useEffect, useState } from 'react'
import { Image } from './components/Image.jsx'
import tyrone from './assets/tyrone.webp'
import uniqua from './assets/uniqua.webp'
import tasha from './assets/tasha.webp'
import austin from './assets/austin.webp'
import pablo from './assets/pablo.jpg'

const pImages = [tyrone, uniqua, pablo, tasha, austin]

const positions = [
  { x: '260px', y: '50px' },
  { x: '450px', y: '200px' },
  { x: '150px', y: '450px' },
  { x: '370px', y: '450px' },
  { x: '60px', y: '200px' },
]

function App() {
  const [philosophers, setPhilosophers] = useState([])

  useEffect(() => {
    const fetchPhilosophers = async () => {
      const response = await fetch('http://127.0.0.1:5000/simulation')

      if (response.ok) {
        const reader = response.body.getReader()
        const decoder = new TextDecoder('utf-8')

        while (true) {
          const { done, value } = await reader.read(); // Lee los datos

          if (done) {
            break; // Si no hay más datos, sal del bucle
          }

          const chunk = decoder.decode(value, { stream: true }); // Decodifica el chunk
          const dataLines = chunk.split('\n'); // Divide el chunk en líneas

          for (const line of dataLines) {
            if (line.startsWith('data:')) { // Verifica si es un dato
              const philosopherState = JSON.parse(line.substring(5).trim()); // Extrae y parsea el estado
              setPhilosophers(prev => philosopherState); // Actualiza el estado de los filósofos
            }
          }

        }
      } else {
        console.error('Something went wrong:', response.status, response.statusText);
      }
    }

    fetchPhilosophers()
  }, [])

  return (
    <>
      <h1 className='text-center text-black font-bold text-2xl'
      >
        Solución ineficiente
      </h1>
      {/* Panel to table and philosophers */}
      <div className='flex items-center relative justify-center w-[600px] h-[640px]'>
        { philosophers?.map((stat, index) => 
          <Image
            src={pImages[index]}
            positionX={positions[index].x}
            positionY={positions[index].y}
            state={stat}
          />
        )}
        <div>
          <img src={ImageMesa}
            className='w-80 h-80 object-fill rounded-full'
          />
        </div>
      </div>
    </>
  )
}

export default App
