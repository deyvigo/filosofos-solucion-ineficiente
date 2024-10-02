export const Image = ({ src, positionX, positionY, state }) => {
  const colors = {
    'pensando': 'text-red-500',
    'hambriento': 'text-yellow-500',
    'comiendo': 'text-green-500',
  }
  return (
    <>
      <div className="absolute w-20 h-20 rounded-full items-center" style={{ left: positionX, top: positionY }}>
        <h1 className={ `text-center font-bold ${colors[state]}` }>{ state.toLocaleUpperCase() }</h1>
        <img src={src} className={ `w-full h-full object-contain rounded-full ${colors[state]}` } />
      </div>
    </>
  )
}