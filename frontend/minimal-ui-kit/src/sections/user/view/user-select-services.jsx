import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';

const UserSelectServices = ({value, onChange}) =>{

    const Authorization = "caea2820b080747d03f33d6899a673df0f71fff2e9cb0f475d198158d7bced3c"
    const [options, setOptions] = useState([]);
    // const [selectedOption, setSelectedOption] = useState('');

    useEffect(() => {
        // Hacer la solicitud a la API para obtener las opciones del select
        const fetchOptions = async () => {
          try {
            const myHeaders = new Headers();
            myHeaders.append("Authorization", Authorization);

            const requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
            };

            const response = await fetch("http://127.0.0.1:5014/servicios", requestOptions);
            const jsonData = await response.json();
            let data_rows = [];
            if(jsonData.estado === 1){
            data_rows = jsonData.data.services
            }
            setOptions(data_rows);
          } catch (error) {
            console.error('Error al obtener opciones del select:', error);
          }
        };
    
        fetchOptions();
      }, []); // Se ejecuta solo una vez al montar el componente
    
    // const handleSelectChange = (event) => {
    // setSelectedOption(event.target.value);
    // };
    
      

  return (
    <>
        <InputLabel id="select-label">Select a service</InputLabel>
        <Select
        labelId="select-label"
        id="service"
        name="service"
        value={value}
        label="Select a service"
        onChange={onChange}
        sx={{ width: '100%' }}
        >
        {options.map((option) => (
            <MenuItem key={option.id} value={option.id}>
            {option.name}
            </MenuItem>
        ))}
        </Select>
    </>
  )
}

UserSelectServices.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
};

export default UserSelectServices