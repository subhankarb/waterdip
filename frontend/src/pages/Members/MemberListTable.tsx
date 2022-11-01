import { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// material
import {
  Table,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
  TableContainer,
  TablePagination
} from '@material-ui/core';
// components
import Scrollbar from '../../components/Scrollbar';
// import { PATH_DASHBOARD } from '../../routes/paths';

// ----------------------------------------------------------------------

interface UserData {
  email: string;
  userName: string;
  role: string;
  joined: string;
}

const USER_ROWS: UserData[] = [
  { email: 'subhankar@waterdip.ai', userName: 'subhankar', role: 'admin', joined: '11 Jun 2021' }
];

interface ModelColumn {
  id: 'email' | 'userName' | 'role' | 'joined';
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const MODEL_COLUMNS: ModelColumn[] = [
  { id: 'email', label: 'Email', minWidth: 170 },
  { id: 'userName', label: 'User\u00a0Name', minWidth: 170 },
  { id: 'role', label: 'User\u00a0Role', minWidth: 170 },
  { id: 'joined', label: 'Joine\u00a0On', minWidth: 170, align: 'right' }
];

// ----------------------------------------------------------------------

export default function UserListTable() {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <>
      <Scrollbar>
        <TableContainer sx={{ minWidth: 800 }}>
          <Table>
            <TableHead>
              <TableRow>
                {MODEL_COLUMNS.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ top: 56, minWidth: column.minWidth }}
                  >
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {USER_ROWS.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
                <TableRow hover role="checkbox" tabIndex={-1} key={row.email}>
                  {MODEL_COLUMNS.map((column) => {
                    const value = row[column.id];
                    return (
                      <TableCell key={column.id} align={column.align}>
                        {column.format && typeof value === 'number' ? column.format(value) : value}
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Scrollbar>

      <TablePagination
        page={page}
        component="div"
        count={USER_ROWS.length}
        rowsPerPage={rowsPerPage}
        onPageChange={handleChangePage}
        rowsPerPageOptions={[10, 25, 100]}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </>
  );
}
