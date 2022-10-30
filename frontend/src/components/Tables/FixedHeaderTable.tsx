import { useState, useEffect } from 'react';
import { Icon } from '@iconify/react';
import trash2Fill from '@iconify/icons-eva/trash-2-fill';
import editFill from '@iconify/icons-eva/edit-fill';
import { v4 as uuidv4 } from 'uuid';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import { Box, Button } from '@material-ui/core';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import { colors } from '../../theme/colors';

const useStyles = makeStyles({
  container: {
    maxHeight: 200
  },
  button: {
    minWidth: 'auto !important',
    marginRight: '0 !important',
    fontSize: '1rem !important',
    padding: '0 .9rem'
  }
});
type Props = {
  data: any;
  onDelete: Function;
  onEdit: Function;
  title: any;
};

const HeaderTable = ({ title, onDelete, data, onEdit }: Props) => {
  const [EditIndex, setEditIndex] = useState<number>();
  const [DeleteIndex, setDeleteIndex] = useState<number>();
  const classes = useStyles();
  const heading = [
    [title, '40%'],
    ['Type', '40%'],
    ['', '20%']
  ];
  useEffect(() => {
    onDelete(DeleteIndex);
  }, [DeleteIndex]);

  useEffect(() => {
    onEdit(EditIndex);
    if (EditIndex) {
      setEditIndex(undefined);
    }
  }, [EditIndex]);

  return (
    <>
      <Box
        component={Paper}
        className={classes.container}
        style={{ overflowX: 'hidden', scrollbarWidth: 'thin' }}
      >
        {data && (
          <Table>
            <TableHead
              style={{
                height: '30px',
                background: colors.tableHeadBack,
                borderRadius: '2px 2px 0px 0px'
              }}
            >
              <TableRow>
                {heading.map((data) => (
                  <TableCell
                    key={uuidv4()}
                    align="center"
                    style={{
                      width: data[1],
                      fontFamily: 'Poppins',
                      fontStyle: 'normal',
                      fontWeight: 500,
                      fontSize: '12px',
                      boxShadow: 'none',
                      color: colors.tableText,
                      background: colors.tableHeadBack
                    }}
                  >
                    {data[0]}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            {Object.entries(data).map((fp: any, index: number) => (
              <TableBody key={index}>
                <TableRow>
                  <TableCell component="th" align="center" scope="row">
                    {fp[0]}
                  </TableCell>
                  <TableCell align="center">{fp[1]}</TableCell>
                  <TableCell
                    align="center"
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      paddingLeft: 0,
                      paddingRight: 0
                    }}
                  >
                    <Button
                      color="primary"
                      size="small"
                      className={classes.button}
                      onClick={() => {
                        setEditIndex(index);
                      }}
                      sx={{ mr: 1 }}
                    >
                      <Icon icon={editFill} />
                    </Button>
                    <Button
                      color="error"
                      size="small"
                      className={classes.button}
                      onClick={() => setDeleteIndex(index)}
                      sx={{ mr: 1 }}
                    >
                      <Icon icon={trash2Fill} />
                    </Button>
                  </TableCell>
                </TableRow>
              </TableBody>
            ))}
          </Table>
        )}
      </Box>
    </>
  );
};

export default HeaderTable;
