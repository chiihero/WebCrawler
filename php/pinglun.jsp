<%@page import="org.json.*"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*"%>
<%
	request.setCharacterEncoding("UTF-8");
%>
<%
	response.setHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");
	response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
	response.setHeader("Access-Control-Allow-Origin", "*");
	//删除
	String driver = "com.mysql.jdbc.Driver";
	String url = "jdbc:mysql://139.199.11.57:3306/weapp?";

	Connection conn = null;
	Statement stmt = null;
	String sql;
	try {
		Class.forName(driver);
		conn = DriverManager.getConnection(url, "weapp", "weapp1");
		stmt = conn.createStatement();

		String action = request.getParameter("u_action");	//得到行为
		String name=request.getParameter("u_name");
		String comment=request.getParameter("u_com");
		
		int flag=1;

		/*显示评论*/
		if(action.equals("display"))
		{
		/*select and display*/
        sql = "select * from pinglun";
        ResultSet rs = stmt.executeQuery(sql);
        //生成一个JSON类 这个类在jsp中显示
      	JSONObject commentJson = new JSONObject();
    	//生成一个JSON类
    	List commentList = new ArrayList();
    	while(rs.next()){
    	//	out.println(rs.getInt(1) + "&nbsp; &nbsp;" + rs.getString(2));
    		JSONObject Pinglun = new JSONObject();
    		Pinglun.put("name",rs.getString(1));
    		Pinglun.put("comment",rs.getString(2));
    		Pinglun.put("time",rs.getInt(3));
    		commentList.add(Pinglun);
    	}
    	
    	commentJson.put("comments",commentList);//http 访问的接口名字comments
    	out.print(commentJson);
    	out.flush();
		}
		
		else if(action.equals("insert"))
		{
			
			/*判断（u_mask）是否评论过*/
			if(name!=null)
			{
				 sql = "select * from userinfo where u_name = '"+name+"'";
				 ResultSet rx = stmt.executeQuery(sql);
				 while(rx.next()){
						String h_name=rx.getString(1);
						flag=rx.getInt(5);
						
						System.out.println("name:"+h_name+"\t u_make:"+flag);
						
						
				    }
			}
			if(flag==0)
			{
				/*添加评论*/
				if(name!=null&&comment != null) {

					//?u_action=insert&u_name=hjh
					flag=1;	
					sql="insert into pinglun(u_name,u_com,c_date)values('"+name
					+"','"+comment+"','2017-06-14 00:00:00')";
					stmt.executeUpdate(sql);
					sql="update userinfo set u_make ='" + flag + "' where u_name='" + name + "'";
					stmt.executeUpdate(sql);

					System.out.println("name:"+name+"\tcomment:"+comment);
				
					}
	   
					else
					{
						
						System.out.println("用户已评论过，不能再次评论！");
					
						
					}
				/*删除评论*/
			//	if(action != null && action.equals("delete") && make != null && make.equals("1")) {
			//		make=1；	
			//		String sql = "delete from pinglun where u_name=" + name + "";
			//		stmt.executeUpdate(sql);
			//	}
				/*修改函数*/
			//	if(action != null && action.equals("update") && make != null && make.equals("1")) {
			//		make=1；	
			//		String sql = "update pinglun set u_com='" + comment + "' where u_name like '%" + name + "%'";
			//		//int result = stmt.executeUpdate(sql);
			//		stmt.executeUpdate(sql);
			//	}			
			}
			else if(flag==1)
			{
				sql = "update pinglun set u_com='" + comment + "' where u_name = '" + name + "'";
				stmt.executeUpdate(sql);				
			}
			else
			{
				System.out.println("请传入合适的参数！");
			}
		}
		
		stmt.close();
		conn.close();
	} catch (SQLException e) {
		out.println("MySQL操作错误！");
		e.printStackTrace();
	} catch (Exception e) {
		out.println("MySQL操作错误！请传入正确的值！ ");
		e.printStackTrace();
	}
%>
