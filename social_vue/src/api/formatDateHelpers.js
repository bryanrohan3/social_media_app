export function formatDate(date) {
  const formattedDate = new Date(date);
  const year = formattedDate.getFullYear();

  if (year === 2024) {
    return (
      formattedDate.toLocaleString("en-US", {
        month: "short",
        day: "numeric",
      }) +
      " at " +
      formattedDate.toLocaleString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })
    );
  } else {
    return (
      formattedDate.toLocaleString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      }) +
      " at " +
      formattedDate.toLocaleString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      })
    );
  }
}
