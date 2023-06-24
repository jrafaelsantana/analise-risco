export default function convertDatetime(str: string) {
  const [dateValues, timeValues] = str.split(" ");
  const [day, month, year] = dateValues.split("/");
  const [hours, minutes, seconds] = timeValues.split(":");

  const date = new Date(+year, +month - 1, +day, +hours, +minutes, +seconds);
  return date;
}
