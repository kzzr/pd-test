import { useState } from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import TextField from '@mui/material/TextField';
import Iconify from 'src/components/iconify';
import TextareaAutosize  from '@mui/material/TextareaAutosize';
import UserSelectServices from './user-select-services';
import UserSelectPriority from './user-select-priority';
import UserSelectEscalation from './user-select-escalation';

const UserModalIncident = ({ onReloadData }) => {
    const Authorization = "caea2820b080747d03f33d6899a673df0f71fff2e9cb0f475d198158d7bced3c"

    const [openModal, setOpenModal] = useState(false);
    const [selectedUrgency, setselectedUrgency] = useState('');

    const [selectService, setselectService] = useState('');
    const [selectPriority, setselectPriority] = useState('');
    const [selectEscalation, setselectEscalation] = useState('');


    const [formData, setFormData] = useState({
    // Define las propiedades del formulario según tus necesidades
    title: '',
    service: '',
    priority: '',
    urgency: '',
    description: '',
    escalation_policy: '',
    // Agrega más campos según las propiedades de tu API
  });

    const handleCloseModal = () => {
        setOpenModal(false);
      };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
    
        try {
          const myHeaders = new Headers();
          myHeaders.append("Authorization", Authorization);
          myHeaders.append("Content-Type", "application/json");
          console.log(selectService)
          console.log(selectPriority)

          const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            let incident_key = '';

            for (let i = 0; i < 32; i += 1) {
                const randomIndex = Math.floor(Math.random() * characters.length);
                incident_key += characters.charAt(randomIndex);
            }
          const payload = {
            "incident": {
              "type": "incident",
              "title": formData.title,
              "service": {
                "id": selectService,
                "type": "service_reference"
              },
              "priority": {
                "id": selectPriority,
                "type": "priority_reference"
              },
              "urgency": selectedUrgency,
              "incident_key": incident_key,
              "body": {
                "type": "incident_body",
                "details": formData.description
              },
              "escalation_policy": {
                "id": selectEscalation,
                "type": "escalation_policy_reference"
              }
            }
          }
          console.log(payload)
          const requestOptions = {
            method: 'POST', // Cambia a 'PUT' o 'PATCH' según sea necesario
            headers: myHeaders,
            body: JSON.stringify(payload),
            redirect: 'follow',
          };
    
          // Realiza la solicitud a la API
          const response = await fetch("http://127.0.0.1:5014/incidencias", requestOptions);
          const jsonData = await response.json();
          console.log(jsonData)
          if (onReloadData) {
            onReloadData();
          }
          handleCloseModal();
        } catch (error) {
          console.error('Error al enviar el formulario a la API:', error);
        }
      };
    
      const handleInputChange = (e) => {
        setFormData({
          ...formData,
          [e.target.name]: e.target.value,
        });
      };
      const handleOpenModal = () => {
        setOpenModal(true);
      };

      
  return (
    <>
        <Button variant="contained" color="inherit" startIcon={<Iconify icon="eva:plus-fill" />} onClick={handleOpenModal}>
            New Incident
        </Button>

        <Modal open={openModal} onClose={handleCloseModal}>
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: 400,
              bgcolor: 'background.paper',
              border: '2px solid #000',
              p: 4,
            }}
          >
            <h3>Add new Incidents</h3>
            <form onSubmit={handleSubmit}>
              <TextField
                label="Title"
                variant="outlined"
                fullWidth
                margin="normal"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
              />
              <UserSelectServices
                value={selectService}
                onChange={(event) => setselectService(event.target.value)}
              />
              <UserSelectPriority
                 value={selectPriority}
                 onChange={(event) => setselectPriority(event.target.value)}
              />
              <InputLabel id="select-label">Select a urgency</InputLabel>
              <Select
                    labelId="select-label"
                    id="urgency"
                    name="urgency"
                    value={selectedUrgency}
                    label="Select a urgency"
                    onChange={(event) => setselectedUrgency(event.target.value)}
                    sx={{ width: '100%' }}
                    >
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="low">Low</MenuItem>
                </Select>
              
              <UserSelectEscalation
                value={selectEscalation}
                onChange={(event) => setselectEscalation(event.target.value)}
              />
              <InputLabel id="select-label">Description</InputLabel>
              <TextareaAutosize
                label="Description"
                variant="outlined"
                margin="normal"
                name="description"
                placeholder="Escribe aquí..."
                value={formData.description}
                onChange={handleInputChange}
                minRows={5} // Establece el número mínimo de filas
                maxRows={10} // Establece el número máximo de filas
                style={{ width: '100%' }}
              />
              {/* Agrega más campos de formulario según las propiedades de tu API */}
              <Button type="submit" variant="contained" color="primary">
                Send
              </Button>
            </form>
          </Box>
        </Modal>
    </>
  )
}
UserModalIncident.propTypes = {
    onReloadData: PropTypes.string.isRequired,
  };
export default UserModalIncident