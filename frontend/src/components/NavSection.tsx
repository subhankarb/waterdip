// material
import { experimentalStyled as styled } from '@material-ui/core/styles';
import { Box, List, ListSubheader, BoxProps } from '@material-ui/core';
// theme
import typography from '../theme/typography';
import NavItem, { NavItemProps } from './NavItem';

// ----------------------------------------------------------------------

const ListSubheaderStyle = styled((props) => (
  <ListSubheader disableSticky disableGutters {...props} />
))(({ theme }) => ({
  ...typography.overline,
  marginTop: theme.spacing(3),
  marginBottom: theme.spacing(2),
  paddingLeft: theme.spacing(5),
  color: theme.palette.text.primary
}));

// ----------------------------------------------------------------------
interface NavSectionProps extends BoxProps {
  navConfig: {
    subheader: string;
    items: NavItemProps[];
  }[];
}

export default function NavSection({ navConfig, ...other }: NavSectionProps) {
  return (
    <Box {...other}>
      {navConfig.map((list) => {
        const { subheader, items } = list;
        return (
          <List key={subheader} disablePadding>
            <ListSubheaderStyle>{subheader}</ListSubheaderStyle>
            {items.map((item: NavItemProps) => (
              <NavItem key={item.title} item={item} />
            ))}
          </List>
        );
      })}
    </Box>
  );
}
