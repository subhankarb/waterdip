// material
import { Container } from '@material-ui/core';
// components
import Page from '../../components/Page';
import UserListTable from './MemberListTable';
import HeaderBreadcrumbs from '../../components/HeaderBreadcrumbs';

// ----------------------------------------------------------------------

export default function Users() {
  return (
    <Page title="Members | Waterdip">
      <Container>
        <HeaderBreadcrumbs heading="Members" links={[{ name: 'Member List' }]} />
        <UserListTable />
      </Container>
    </Page>
  );
}
