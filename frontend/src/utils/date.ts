export const formatDateTime = (d: Date) => {
  // const currentYear = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(new Date());
  const ye = new Intl.DateTimeFormat('en', { year: 'numeric' }).format(d);
  const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(d);
  const da = new Intl.DateTimeFormat('en', { day: 'numeric' }).format(d);
  // const hour = new Intl.DateTimeFormat('en', { hour: '2-digit', hour12: false }).format(d);
  let min = new Intl.DateTimeFormat('en', { minute: '2-digit', hour12: false }).format(d);
  if (parseInt(min, 10) < 10) min = `0${min}`;
  // return currentYear === ye ? `${mo} ${da}, ${hour}:${min}` : `${mo} ${da}, ${ye}, ${hour}:${min}`;
  return `${mo} ${da} ${ye}`;
};

export const formattedDate = (date: string) => {
  const months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  const d = new Date(date);
  const month = months[d.getMonth()];
  const day = d.getDate();
  const year = d.getFullYear();
  return `${day} ${month} ${year}`;
};

export const computeDateRange = (firstDate: Date | null, secondDate: Date | null) => {
  if (!firstDate || !secondDate) return null;
  const [fromDate, toDate] =
    firstDate.getTime() > secondDate.getTime() ? [secondDate, firstDate] : [firstDate, secondDate];
  const timeDiff = toDate.getTime() - fromDate.getTime();
  const yearsDiff = toDate.getFullYear() - fromDate.getFullYear();
  if (yearsDiff) return `${yearsDiff}Y`;

  let monthsDiff = yearsDiff * 12;
  monthsDiff -= fromDate.getMonth();
  monthsDiff += toDate.getMonth();
  if (monthsDiff > 0) return `${monthsDiff}M`;

  const daysDiff = timeDiff / (1000 * 3600 * 24);
  if (daysDiff) return `${daysDiff}d`;

  const hoursDiff = timeDiff / (1000 * 3600);
  if (hoursDiff) return `${hoursDiff}h`;

  const minutesDiff = timeDiff / (1000 * 60);
  if (minutesDiff) return `${minutesDiff}m`;

  const secondsDiff = timeDiff / 1000;
  return `${secondsDiff}s`;
};
