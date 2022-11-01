import { Icon } from '@iconify/react';
import searchFill from '@iconify/icons-eva/search-fill';
// import roundFilterList from '@iconify/icons-ic/round-filter-list';
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { PATH_DASHBOARD } from '../../../routes/paths';
import { Link as RouterLink } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
// import plusFill from '@iconify/icons-eva/plus-fill';
import { useState, useEffect } from 'react';
import { DialogAnimate } from '../../../components/animate';
import CreateModelDialogue from '.././ModelCreate/CreateModelDialogue';

import { Box, OutlinedInput, InputAdornment, Button } from '@material-ui/core';
import { colors } from '../../../theme/colors';

const SearchStyle = styled(OutlinedInput)(({ theme }) => ({
  width: 360,
  height: 40,
  borderRadius: 4,
  background: '#fff',
  transition: theme.transitions.create(['box-shadow', 'width'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.shorter
  }),
  '&.Mui-focused': { width: 360, boxShadow: theme.customShadows.z8 },
  '& fieldset': {
    borderWidth: `1px !important`,
    borderColor: `${theme.palette.grey[500_32]} !important`
  }
}));

type ModelListToolbarProps = {
  searchName: string;
  onSearch: (value: string) => void;
  forceUpdate: any;
};
const useStyles = makeStyles(() => ({
  modellist_toolbar_container: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1.75rem 0rem'
  },
  toolbar_search_filter: {
    display: 'flex',
    alignItems: 'center'
  },
  search: {
    marginRight: '1.2rem'
  },

  toolbar_add_btn: {},
  button_add: {
    fontSize: '0.75rem',
    fontWeight: 600,
    letterSpacing: '0.01em',
    color: colors.white,
    background: colors.textPrimary,
    boxShadow: '0px 4px 10px rgba(103, 128, 220, 0.24)',
    borderRadius: '4px',
    height: '40px',
    padding: '0rem 2.4rem'
  }
}));

const DialogBox = ({ handleClick, forceUpdate }: any) => {
  const classes = useStyles();
  const [boxDisplay, setBoxDisplay] = useState(true);

  return (
    <>
      {boxDisplay === true ? (
        <>
          <CreateModelDialogue handleClick={handleClick} forceUpdate={forceUpdate} />
        </>
      ) : null}
    </>
  );
};

export default function UserListToolbar({
  searchName,
  onSearch,
  forceUpdate
}: ModelListToolbarProps) {
  const classes = useStyles();
  const [value, setValue] = useState(searchName);
  const [expandForm, setExpandForm] = useState(false);
  useEffect(() => {
    onSearch(value);
  }, [value, expandForm]);
  const handleClick = () => {
    setExpandForm(false);
  };
  return (
    <div className={classes.modellist_toolbar_container}>
      <div className={classes.toolbar_search_filter}>
        <div className={classes.search}>
          <SearchStyle
            value={searchName}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Search "
            startAdornment={
              <InputAdornment position="start">
                <Box component={Icon} icon={searchFill} sx={{ color: 'text.disabled' }} />
              </InputAdornment>
            }
          />
        </div>
      </div>
      <div className={classes.toolbar_add_btn}>
        <Button
          className={classes.button_add}
          variant="contained"
          onClick={() => setExpandForm((state) => !state)}
        >
          Add Model
        </Button>
        <DialogAnimate maxWidth="sm" open={expandForm} onClose={() => setExpandForm(false)}>
          <DialogBox handleClick={handleClick} forceUpdate={forceUpdate} />
        </DialogAnimate>
      </div>
    </div>
  );
}
