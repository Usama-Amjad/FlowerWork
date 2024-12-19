import React, { useEffect, useState } from 'react'
import {useParams} from 'react-router-dom'
import icon from '../assets/back.png'

const Player = () => {
    const {id} = useParams()

    const [apiData,setApiData] =useState({
        name:"",
        key:"",
        published_at:"",
        type:""
    })

    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyOGYxZTI4NjUzMjRjZGMxMGNkZTgzMjJiZGUzMjQ1MCIsInN1YiI6IjY2NjgyNzQyMTBlMmRjMDdhMjFjNDJhMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.0suZlye7b_ajKWIdBkoxMKYCapbmWUlRI31i5VwktNk'
        }
      };

      
      
    useEffect(()=>{
        fetch(`https://api.themoviedb.org/3/movie/${id}/videos?language=en-US`, options)
        .then(response => response.json())
        .then(response => setApiData(response.results[0]))
        .catch(err => console.error(err));
    },[])

    console.log(apiData)

  return (
    <div>
      <div className='flex flex-col justify-center items-center h-[1000px]'>
        <iframe className='rounded-lg' width='95%' height='84%' src={`https://www.youtube.com/embed/${apiData.key}`}
         frameBorder="0" title='trailer' allowFullScreen></iframe>
        <div className='text-white flex justify-between items-center w-[90%]'>
            <p className='text-xl mt-2'>{apiData.name}</p>
            <p className='text-xl mt-2'>{apiData.type}</p>  
            <p className='text-xl mt-2'>{apiData.published_at.slice(0,10)}</p>    
        </div>      
      </div>
    </div>
    
  )
}

export default Player
