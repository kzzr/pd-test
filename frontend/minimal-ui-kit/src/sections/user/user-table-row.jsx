import { useState } from 'react';
import PropTypes from 'prop-types';

import Stack from '@mui/material/Stack';
import Popover from '@mui/material/Popover';
import TableRow from '@mui/material/TableRow';
import Checkbox from '@mui/material/Checkbox';
import MenuItem from '@mui/material/MenuItem';
import TableCell from '@mui/material/TableCell';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';

import Label from 'src/components/label';
import Iconify from 'src/components/iconify';

// ----------------------------------------------------------------------

export default function UserTableRow({
  id,
  title,
  service,
  status,
  urgency,
  created_at,
  selected,
  handleClick,
  onReloadData,
}) {

  const newStatus1 = status ==="triggered" ? 'resolved' : 'acknowledged'
  const newStatus2 = status ==="resolved" ? 'triggered' : 'acknowledged'

  const [open, setOpen] = useState(null);
  const Authorization = "caea2820b080747d03f33d6899a673df0f71fff2e9cb0f475d198158d7bced3c"
  const handleOpenMenu = (event) => {
    setOpen({
      anchorEl: event.currentTarget,
      rowData: { id, title, service, status, urgency, created_at },
    });
  };

  const handleCloseMenu = async(rowData, newstatus) => {
    setOpen(null);
    // Realiza las operaciones necesarias con los datos del row seleccionado
    try {
      const myHeaders = new Headers();
      myHeaders.append("Authorization", Authorization);
      myHeaders.append("Content-Type", "application/json");
      
      const payload = {
          "id": rowData.id,
          "incident": {
              "type": "incident",
              "status": newstatus
          }
      }
      console.log(payload)
      const requestOptions = {
        method: 'PUT', // Cambia a 'PUT' o 'PATCH' según sea necesario
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
    } catch (error) {
      console.error('Error al enviar el formulario a la API:', error);
    }

  };



  return (
    <>
      <TableRow hover tabIndex={-1} role="checkbox" selected={selected}>
        <TableCell padding="checkbox">
          <Checkbox disableRipple checked={selected} onChange={handleClick} />
        </TableCell>

        <TableCell component="th" scope="row" padding="none">
          <Stack direction="row" alignItems="center" spacing={2}>
            
            <Typography variant="subtitle2" noWrap>
              {id}
            </Typography>
          </Stack>
        </TableCell>

        <TableCell>{title}</TableCell>
        <TableCell>{service}</TableCell>
        <TableCell>{created_at}</TableCell>
        <TableCell>{status}</TableCell>


        <TableCell>
          <Label color={(urgency === 'high' && 'error') || 'warning'}>{urgency}</Label>
        </TableCell>

        <TableCell align="right">
          <IconButton onClick={handleOpenMenu}>
            <Iconify icon="eva:more-vertical-fill" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
        open={!!open}
        anchorEl={open?.anchorEl}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: { width: 160 },
        }}
      >
        <MenuItem
          onClick={() => handleCloseMenu(open?.rowData,newStatus1)}
          sx={{ color: 'success.main' }}
        >
          <Iconify icon="mingcute:check-fill" sx={{ mr: 2 }} />
          {newStatus1}
        </MenuItem>

        <MenuItem
          onClick={() => handleCloseMenu(open?.rowData,newStatus2)}
          sx={{ color: 'info.main' }}
        >
          <Iconify icon="simple-icons:answer" sx={{ mr: 2 }} />
          {newStatus2}
        </MenuItem>
      </Popover>
    </>
  );
}


UserTableRow.propTypes = {
  id: PropTypes.string,
  title: PropTypes.string,
  service: PropTypes.string,
  status: PropTypes.string,
  urgency: PropTypes.string,
  created_at: PropTypes.string,
  selected: PropTypes.any,
  handleClick: PropTypes.func,
  onReloadData: PropTypes.func,
};
