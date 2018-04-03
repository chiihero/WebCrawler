<%@ page language="java" import="org.json.*"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*"%>
<%
	request.setCharacterEncoding("UTF-8");
%>
<%
	response.setHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");
	response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
	response.setHeader("Access-Control-Allow-Origin", "*");
%>
<%
	Connection conn = null;
	String sql;

	String url = "jdbc:mysql://139.199.11.57:3306/weapp?"
			+ "user=weapp&password=weapp1&useUnicode=true&characterEncoding=UTF8";

	try {

		Class.forName("com.mysql.jdbc.Driver");// 动态加载mysql驱动

		// 一个Connection代表一个数据库连接

		conn = DriverManager.getConnection(url);
		Statement stmt = conn.createStatement();

		sql = "SELECT * FROM piaoshu";//获取数据库内容
		
		ResultSet rs = stmt.executeQuery(sql);//执行结果，返回到rs
		
		JSONObject ballotListJson=new JSONObject(); 
		
		List ballotList= new ArrayList();
			
		while (rs.next()) 
		{
			
			JSONObject ballot = new JSONObject();
			
			ballot.put("Id",rs.getString(2));
			ballot.put("p_count",rs.getString(3));
			
			ballotList.add(ballot);
					
		}
		
		ballotListJson.put("cities",ballotList);
		
		out.print(ballotListJson);
		out.flush();
		
		stmt.close();

		conn.close();

	} catch (SQLException e) {
		out.println("MySQL操作错误");
		e.printStackTrace();

	} catch (Exception e) {
		out.println("MySQL操作错误");
		e.printStackTrace();

	} finally {

		try {
			conn.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
%>