view: example {
  view_name: Example
  sql_table_name: looker.sp.example ;;

  dimension: id {
    sql: ${TABLE}.id ;;
    type: number
    label: "ID"
    primary_key: yes
  }

  dimension: start_tstamp {
    sql: ${TABLE}.start_tstamp ;;
    type: time
    label: "Start"
    convert_tz: no
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year,
    ]
  }

  dimension: addresses {
    sql: ${TABLE}.addresses ;;
    label: "Addresses"
    hidden: yes
  }
}

view: {
  view_name: example__addresses

  dimension: status {
    sql: status ;;
    type: string
    label: "Status"
    description: "Some sort of status field here."
    group_label: "Addresses"
  }
}