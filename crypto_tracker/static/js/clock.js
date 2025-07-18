function updateTimeAndDate() {
  const now = new Date();

  // clock in 12-hour-format with AM/PM
  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12; // 0 will to 12

  const timeString = `${hours}:${minutes}:${seconds} ${ampm}`;
  document.getElementById('clock').textContent = timeString;

  // Date in format: weekday, dd.mm.yyyy
  // const days = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  // const dayName = days[now.getDay()];
  const day = String(now.getDate()).padStart(2, '0');
  const month = String(now.getMonth() + 1).padStart(2, '0'); // month from 0-11
  const year = now.getFullYear();

  //const dateString = `${dayName}, ${day}.${month}.${year}`;
  const dateString = `${day}.${month}.${year}`;
  document.getElementById('date').textContent = dateString;
}

updateTimeAndDate();
setInterval(updateTimeAndDate, 1000);